import typing
from http import HTTPStatus

import requests

from common.py.component.backend_component import BackendComponent
from common.py.core.messaging.channel import Channel
from common.py.core.messaging.composers.message_builder import MessageBuilder
from common.py.data.entities.project.logbook.project_job_history_record import (
    ProjectJobHistoryRecordExtData,
    ProjectJobHistoryRecordExtDataIDs,
)
from common.py.data.entities.project.project_external_state import (
    check_reuse_external_project,
    ProjectExternalState,
)
from common.py.data.entities.resource.resource import Resource
from common.py.data.entities.resource.resource_utils import (
    files_list_from_resources_list,
)
from common.py.data.entities.resource.resources_list import ResourcesList
from common.py.integration.resources.brokers.tunnels.memory_broker_tunnel import (
    memory_broker_tunnel_from_data,
    MemoryBrokerTunnel,
)
from common.py.integration.resources.transmitters import (
    ResourcesTransmitterDownloadCallbacks,
)
from common.py.integration.resources.transmitters.resources_transmitter_callbacks import (
    ResourceBuffer,
    ResourcesTransmitterPrepareCallbacks,
)
from common.py.services.service import Service
from common.py.utils.paths import relativize_path
from common.py.utils.strings import human_readable_file_size
from connectors.base.data.entities.connector.connector_job import ConnectorJob
from connectors.base.data.types.callbacks import ProjectExternalStateCallbacks
from connectors.base.execution.connector_job_executor import ConnectorJobExecutor
from connectors.dataverse.dataverse.dataverse_callbacks import (
    DataverseCreateCollectionCallbacks,
    DataverseCreateDatasetCallbacks,
    DataverseDeleteAllFilesCallbacks,
    DataverseGetDatasetCallbacks,
    DataverseGetUserCallbacks,
    DataverseQueryCollectionCallbacks,
    DataverseUpdateDatasetCallbacks,
    DataverseUploadFileCallbacks,
)
from connectors.dataverse.dataverse.dataverse_client import DataverseClient
from connectors.dataverse.dataverse.dataverse_request_data import (
    DataverseCollectionObject,
    DataverseCreateDatasetObject,
    DataverseDatasetObject,
    DataverseDatasetVersionObject,
    DataverseFileObject,
    DataverseUserObject,
)


class DataverseJobExecutor(ConnectorJobExecutor):
    """
    Job executor for Dataverse.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        job: ConnectorJob,
        *,
        message_builder: MessageBuilder,
        target_channel: Channel,
    ):
        super().__init__(
            comp,
            svc,
            job,
            message_builder=message_builder,
            target_channel=target_channel,
            tunnel_type=MemoryBrokerTunnel,
        )

        self._dataverse_client = DataverseClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self.job.user_token,
        )

        self._reuse_external_project = False

    def start(self, external_state: ProjectExternalState) -> None:
        self._reuse_external_project = check_reuse_external_project(external_state)
        self._get_user(external_state=external_state)

    # -- External state

    def query_external_project_state(
        self,
        external_state: ProjectExternalState,
        *,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        self.report_message("Querying external dataset...")

        callbacks = DataverseGetDatasetCallbacks()
        callbacks.done(
            lambda data: self._query_external_project_state_done(data, state_callbacks)
        )
        callbacks.failed(
            lambda exc: self._query_external_project_state_failed(exc, state_callbacks)
        )

        self._dataverse_client.get_dataset(
            dataset_id=external_state.external_id, callbacks=callbacks
        )

    def _query_external_project_state_done(
        self,
        dataverse_dataset: DataverseDatasetObject,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        from .dataverse_utils import process_external_project_state

        external_state = ProjectExternalState(
            external_id=dataverse_dataset.id,
            external_state=ProjectExternalState.State.UNKNOWN,
        )
        process_external_project_state(dataverse_dataset, external_state)

        state_callbacks.invoke_done_callbacks(external_state)

    def _query_external_project_state_failed(
        self,
        exc: Exception,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        if isinstance(exc, requests.exceptions.RequestException) and (
            exc.response.status_code == HTTPStatus.NOT_FOUND
            or exc.response.status_code == HTTPStatus.GONE
        ):
            self.report_message(
                "The previous dataset no longer exists, a new one will be created"
            )

            state_callbacks.invoke_done_callbacks(
                ProjectExternalState(
                    external_id="",
                    external_state=ProjectExternalState.State.DEFAULT,
                )
            )
        else:
            state_callbacks.invoke_fail_callbacks(str(exc))

    # User handling

    def _get_user(self, *, external_state: ProjectExternalState) -> None:
        self.report_message("Getting user...")

        callbacks = DataverseGetUserCallbacks()
        callbacks.done(
            lambda data: self._get_user_done(data, external_state=external_state)
        )
        callbacks.failed(lambda exc: self._get_user_failed(exc))

        self._dataverse_client.get_user(callbacks=callbacks)

    def _get_user_done(
        self,
        dataverse_user: DataverseUserObject,
        *,
        external_state: ProjectExternalState,
    ):
        self.report_message(f"Found user {dataverse_user.user_identifier}")

        self._get_collection(dataverse_user, external_state=external_state)

    def _get_user_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to find a user for the given API-Token: {str(exc)}")

    # Collection handling

    def _get_collection(
        self,
        dataverse_user: DataverseUserObject,
        *,
        external_state: ProjectExternalState,
    ) -> None:
        self.report_message(
            f"Getting collection for user {dataverse_user.user_identifier}..."
        )

        callbacks = DataverseQueryCollectionCallbacks()
        callbacks.done(
            lambda data: self._get_collection_done(data, external_state=external_state)
        )
        callbacks.failed(
            lambda _: self._get_collection_failed(
                dataverse_user, external_state=external_state
            )
        )

        collection_id = dataverse_user.user_identifier.lstrip("@")
        self._dataverse_client.get_collection(
            collection_id=collection_id,
            callbacks=callbacks,
        )

    def _get_collection_done(
        self,
        dataverse_user_collection: DataverseCollectionObject,
        *,
        external_state: ProjectExternalState,
    ) -> None:
        if self.is_active:
            if self._reuse_external_project:
                self._dataset_update(external_state)
            else:
                self._dataset_create(dataverse_user_collection)

    def _get_collection_failed(
        self,
        dataverse_user: DataverseUserObject,
        *,
        external_state: ProjectExternalState,
    ) -> None:
        self.report_message(
            f"Creating collection for user {dataverse_user.user_identifier}..."
        )

        callbacks = DataverseCreateCollectionCallbacks()
        callbacks.done(
            lambda data: self._get_collection_done(data, external_state=external_state)
        )
        callbacks.failed(lambda exc: self._create_collection_failed(exc))

        collection_id = dataverse_user.user_identifier.lstrip("@")
        self._dataverse_client.create_collection(
            "demo",  # TODO parent collection: is there a way to get the root collection of a dataverse instance?
            collection_name=dataverse_user.user_display_name,
            collection_id=collection_id,
            collection_contact=dataverse_user.user_email,
            callbacks=callbacks,
        )

    def _create_collection_failed(self, exc: Exception) -> None:
        self.set_failed(f"Could not create a collection: {str(exc)}")

    # -- Dataset creation

    def _dataset_create(
        self,
        dataverse_user_collection: DataverseCollectionObject,
    ) -> None:
        self.report_message("Creating dataset...")

        callbacks = DataverseCreateDatasetCallbacks()
        callbacks.done(lambda data: self._dataset_create_done(data))
        callbacks.failed(lambda exc: self._dataset_create_failed(exc))

        self._dataverse_client.create_dataset(
            dataverse_user_collection.alias, self._job.project, callbacks=callbacks
        )

    def _dataset_create_done(
        self, dataverse_dataset: DataverseCreateDatasetObject
    ) -> None:
        self.report_message(f"Dataset created (Dataverse ID: {dataverse_dataset.id})")

        self._dataset_get_after_create(dataverse_dataset)

    def _dataset_create_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to create dataset: {str(exc)}")

    def _dataset_get_after_create(
        self, dataverse_dataset: DataverseCreateDatasetObject
    ) -> None:
        self.report_message("Getting created dataset...")

        callbacks = DataverseGetDatasetCallbacks()
        callbacks.done(lambda data: self._dataset_get_after_create_done(data))
        callbacks.failed(lambda exc: self._dataset_get_after_create_failed(exc))

        self._dataverse_client.get_dataset(
            dataset_id=dataverse_dataset.id, callbacks=callbacks
        )

    def _dataset_get_after_create_done(
        self, dataverse_dataset: DataverseDatasetObject
    ) -> None:
        self.report_message("Getting updated dataset...")

        self._transmitter_prepare(dataverse_dataset)

    def _dataset_get_after_create_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to retrieve created dataset: {str(exc)}")

    # -- Dataset update

    def _dataset_update(
        self,
        external_state: ProjectExternalState,
    ) -> None:
        self.report_message("Updating dataset...")

        callbacks = DataverseUpdateDatasetCallbacks()
        callbacks.done(lambda data: self._dataset_update_done(data))
        callbacks.failed(lambda exc: self._dataset_update_failed(exc))

        self._dataverse_client.update_dataset(
            external_state.external_id, self._job.project, callbacks=callbacks
        )

    def _dataset_update_done(
        self, dataverse_dataset: DataverseDatasetVersionObject
    ) -> None:
        self.report_message(f"Dataset updated (Dataverse ID: {dataverse_dataset})")

        self._dataset_update_cleanup(dataverse_dataset)

    def _dataset_update_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to update dataset: {str(exc)}")

    def _dataset_update_cleanup(
        self, dataverse_dataset: DataverseDatasetVersionObject
    ) -> None:
        self.report_message("Clearing previous dataset files...")

        callbacks = DataverseDeleteAllFilesCallbacks()
        callbacks.done(lambda _: self._dataset_update_cleanup_done(dataverse_dataset))
        callbacks.failed(lambda exc: self._dataset_update_cleanup_failed(exc))

        self._dataverse_client.delete_all_files(dataverse_dataset, callbacks=callbacks)

    def _dataset_update_cleanup_done(
        self, dataverse_dataset: DataverseDatasetVersionObject
    ) -> None:
        self.report_message("Dataset cleaned up")

        self._dataset_get_after_cleanup(dataverse_dataset)

    def _dataset_update_cleanup_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to delete dataset files: {str(exc)}")

    def _dataset_get_after_cleanup(
        self, dataverse_dataset_version: DataverseDatasetVersionObject
    ) -> None:
        self.report_message("Getting updated dataset...")

        callbacks = DataverseGetDatasetCallbacks()
        callbacks.done(lambda data: self._dataset_get_after_update_done(data))
        callbacks.failed(lambda exc: self._dataset_get_after_update_failed(exc))

        self._dataverse_client.get_dataset(
            dataset_id=dataverse_dataset_version.dataset_id, callbacks=callbacks
        )

    def _dataset_get_after_update_done(
        self, dataverse_dataset: DataverseDatasetObject
    ) -> None:
        self.report_message(
            f"Retrieved updated dataset (Dataverse ID: {dataverse_dataset.id})"
        )

        self._transmitter_prepare(dataverse_dataset)

    def _dataset_get_after_update_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to retrieve updated dataset: {str(exc)}")

    # -- Transmitter preparation

    def _transmitter_prepare(self, dataverse_dataset: DataverseDatasetObject) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(
            lambda res: self._transmitter_prepare_done(dataverse_dataset, resources=res)
        )
        callbacks.failed(lambda exc: self._transmitter_prepare_failed(exc))
        callbacks.failed(lambda _: self._delete_failed_project(dataverse_dataset))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _transmitter_prepare_done(
        self,
        dataverse_dataset: DataverseDatasetObject,
        *,
        resources: ResourcesList,
    ) -> None:
        files_list = files_list_from_resources_list(resources)

        if len(files_list) > 0:
            self.report_message(
                f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
            )

            self._download_files(dataverse_dataset, files=files_list)
        else:
            self.set_done(
                dataverse_dataset.id, ext_data=self._get_job_ext_data(dataverse_dataset)
            )

    def _transmitter_prepare_failed(self, exc: Exception) -> None:
        self.set_failed(f"Failed to prepare job: {str(exc)}")

    # -- File transfers

    def _download_files(
        self,
        dataverse_dataset: DataverseDatasetObject,
        *,
        files: typing.List[Resource],
    ) -> None:
        def _report_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        callbacks = ResourcesTransmitterDownloadCallbacks()
        callbacks.progress(_report_file)
        callbacks.done(
            lambda res, buffer: self._download_file_done(
                dataverse_dataset, resource=res, buffer=buffer
            )
        )
        callbacks.failed(lambda res, exc: self._download_file_failed(res, exc))
        callbacks.failed(lambda _, __: self._delete_failed_project(dataverse_dataset))
        callbacks.all_done(
            lambda success: (
                self._upload_additional_files(dataverse_dataset) if success else None
            )
        )

        self._transmitter.download_list(files, callbacks=callbacks)

    def _download_file_done(
        self,
        dataverse_dataset: DataverseDatasetObject,
        *,
        resource: Resource,
        buffer: ResourceBuffer,
    ) -> None:
        self.report_message(f"Uploading {resource.filename}...")

        callbacks = DataverseUploadFileCallbacks()
        callbacks.done(lambda data: self._upload_file_done(resource, data))
        callbacks.failed(lambda exc: self._upload_file_failed(resource, exc))
        callbacks.failed(lambda _: self._delete_failed_project(dataverse_dataset))

        self._dataverse_client.upload_file(
            dataverse_dataset=dataverse_dataset,
            path=relativize_path(resource.filename, self._job.project.resources_path),
            file_data=buffer,
            callbacks=callbacks,
        )

    def _download_file_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to download {res.filename}: {str(exc)}")

    def _upload_file_done(self, resource: Resource, _: DataverseFileObject) -> None:
        self.report_message(f"Uploaded {resource.filename}")

    def _upload_file_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to upload {res.filename}: {str(exc)}")

    def _upload_additional_files(
        self, dataverse_dataset: DataverseDatasetObject
    ) -> None:
        self.report_message(f"Uploading additional files...")

        for path, file_data in self._job.additional_files.items():
            self.report_message(f"Uploading {path}...")

            callbacks = DataverseUploadFileCallbacks()
            callbacks.done(lambda data: self._upload_additional_file_done(path, data))
            callbacks.failed(lambda exc: self._upload_additional_file_failed(path, exc))

            self._dataverse_client.upload_file(
                dataverse_dataset=dataverse_dataset,
                path=path,
                file_data=memory_broker_tunnel_from_data(path, file_data),
                callbacks=callbacks,
            )
        else:
            self.set_done(
                str(dataverse_dataset.id),
                ext_data=self._get_job_ext_data(dataverse_dataset),
            )

    def _upload_additional_file_done(self, path: str, _: DataverseFileObject) -> None:
        self.report_message(f"Uploaded {path}")

    def _upload_additional_file_failed(self, path: str, exc: Exception) -> None:
        self.set_failed(f"Failed to upload {path}: {str(exc)}")

    # Miscellaneous

    def _delete_failed_project(self, dataverse_dataset: DataverseDatasetObject) -> None:
        if not self._reuse_external_project:
            self._dataverse_client.delete_dataset_draft(dataverse_dataset)

    def _get_job_ext_data(
        self, dataverse_dataset: DataverseDatasetObject
    ) -> ProjectJobHistoryRecordExtData:
        # Dataverse doesn't provide a direct link itself, so we have to put it together manually
        url = self._dataverse_client.base_url.replace("/api", "").rstrip("/")
        url += f"/dataset.xhtml?persistentId=doi:{dataverse_dataset.authority}/{dataverse_dataset.identifier}&version=DRAFT"

        return {
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_ID: dataverse_dataset.id,
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_LINK: url,
        }
