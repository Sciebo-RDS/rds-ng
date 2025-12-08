import dataclasses
import json
import pathlib
from pathlib import PurePosixPath

import requests

from common.py.component.backend_component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.authorization.authorization_token import AuthorizationToken
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project.project import Project
from common.py.data.entities.user import UserToken
from common.py.integration.authorization.strategies.authorization_strategy import (
    AuthorizationStrategy,
)
from common.py.integration.resources.transmitters import ResourceBuffer
from common.py.services import Service
from connectors.base.integration.execution.requests_executor import (
    RequestsExecutor,
)
from connectors.dataverse.dataverse.dataverse_callbacks import (
    DataverseCreateCollectionCallbacks,
    DataverseCreateDatasetCallbacks,
    DataverseDeleteAllFilesCallbacks,
    DataverseDeleteDatasetDraftCallbacks,
    DataverseGetDatasetCallbacks,
    DataverseGetFileListCallbacks,
    DataverseGetUserCallbacks,
    DataverseQueryCollectionCallbacks,
    DataverseUpdateDatasetCallbacks,
    DataverseUploadFileCallbacks,
)
from connectors.dataverse.dataverse.dataverse_request_data import (
    DataverseCollectionObject,
    DataverseCreateDatasetObject,
    DataverseDatasetObject,
    DataverseDatasetVersionObject,
    DataverseDeleteAllFilesData,
    DataverseFileListObject,
    DataverseFileObject,
    DataverseRequestData,
    DataverseUserObject,
)
from connectors.dataverse.metadata.dataverse_metadata import DataverseMetadataBuilder


class DataverseClient(RequestsExecutor):
    """
    Client to use the Dataverse API.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        connector_instance: ConnectorInstanceID,
        auth_channel: Channel,
        user_token: UserToken,
        max_attempts: int = 1,
        attempts_delay: float = 3.0,
    ):
        """
        Args:
            comp (BackendComponent): The global component.
            svc (Service): The service used for message sending.
            connector_instance (ConnectorInstanceID): The connector instance ID.
            auth_channel (Channel): Channel to fetch authorization tokens from.
            user_token (UserToken): The user token.
            max_attempts (int, optional): The number of attempts for each operation; cannot be lass than 1. Defaults to 1.
            attempts_delay (float, optional): The delay (in seconds) between each attempt. Defaults to 3.0.
        """
        from ...base.settings import ConnectorSettingIDs

        super().__init__(
            comp,
            svc,
            connector_instance=connector_instance,
            auth_channel=auth_channel,
            user_token=user_token,
            base_url=comp.data.config.value(ConnectorSettingIDs.TARGET),
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )

    def get_user(
        self,
        *,
        callbacks: DataverseGetUserCallbacks = DataverseGetUserCallbacks(),
    ) -> None:
        """
        Gets information about the user.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#get-user-information-in-json-format

        Args:
            callbacks (DataverseGetUserCallbacks, optional): _description_. Defaults to DataverseGetUserCallbacks().
        """

        def _execute(session: requests.Session) -> DataverseUserObject:
            resp = self.get(session, ["users", ":me"])

            return DataverseRequestData.data_from_response(DataverseUserObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_collection(
        self,
        collection_id: str,
        *,
        callbacks: DataverseQueryCollectionCallbacks,
    ) -> None:
        """
        Gets a Dataverse Collection.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id31

        Args:
            callbacks (DataverseGetDatasetCallbacks): Optional Callbacks.
            collection_id (str): The ID of the collection to be queried.
        """

        def _execute(session: requests.Session) -> DataverseCollectionObject:
            resp = self.get(session, ["dataverses", collection_id])
            return DataverseRequestData.data_from_response(
                DataverseCollectionObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def create_collection(
        self,
        collection_parent: str,
        collection_name: str,
        collection_id: str,
        collection_contact: str,
        *,
        callbacks: DataverseCreateCollectionCallbacks,
    ) -> None:
        """
        Creates a Dataverse Collection.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#create-a-dataverse-collection

        Args:
            collection_parent (str): The parent collection for the new collection. E.g. root.
            collection_name (str): The display name for the new collection.
            collection_id (str): The ID (also called alias) for the new collection.
            collection_contact: The contact email address for the new collection.
            callbacks (DataverseGetDatasetCallbacks): Optional Callbacks.
        """

        def _execute(session: requests.Session) -> DataverseCollectionObject:
            resp = self.post(
                session,
                ["dataverses", collection_parent],
                json={
                    "name": collection_name,  # e.g. Display name of user
                    "alias": collection_id,  # e.g. id of user
                    "dataverseContacts": [{"contactEmail": collection_contact}],
                },
            )
            return DataverseRequestData.data_from_response(
                DataverseCollectionObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_dataset(
        self,
        dataset_id: str,
        *,
        callbacks: DataverseGetDatasetCallbacks,
    ) -> None:
        """
        Gets the information on an already uploaded dataset.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id80

        Args:
            dataset_id (str): The ID of the dataset.
            callbacks (DataverseGetDatasetCallbacks): Optional Callbacks.
        """

        def _execute(session: requests.Session) -> DataverseDatasetObject:
            resp = self.get(session, ["datasets", dataset_id])

            return DataverseRequestData.data_from_response(DataverseDatasetObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def create_dataset(
        self,
        user_collection_alias: str,
        project: Project,
        *,
        callbacks: DataverseCreateDatasetCallbacks,
    ):
        """
        Creates a Dataverse dataset.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id57

        Args:
            user_collection_alias (str): The collection alias.
            project: The originating project.
            callbacks (DataverseCreateDatasetCallbacks): Optional request callbacks.
        """

        def _execute(session: requests.Session) -> DataverseCreateDatasetObject:
            resp = self.post(
                session,
                ["dataverses", user_collection_alias, "datasets"],
                json=self._get_project_metadata(project),
            )

            return DataverseRequestData.data_from_response(
                DataverseCreateDatasetObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def update_dataset(
        self,
        dataverse_dataset_id: str,
        project: Project,
        *,
        callbacks: DataverseUpdateDatasetCallbacks = DataverseUpdateDatasetCallbacks(),
    ) -> None:
        """
        Updates the metadata of a Dataverse Dataset.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id93

        Args:
            dataverse_dataset_id (str): The persistent id (DOI) of the dataset project.
            project (Project): The rds project.
            callbacks (DataverseUpdateDatasetCallbacks): Optional request callbacks.
        """

        def _execute(session: requests.Session) -> DataverseDatasetVersionObject:
            resp = self.put(
                session,
                ["datasets", dataverse_dataset_id, "versions", ":draft"],
                json=self._get_project_metadata(project).get("datasetVersion"),
            )

            return DataverseRequestData.data_from_response(
                DataverseDatasetVersionObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_all_files(
        self,
        dataverse_dataset: DataverseDatasetVersionObject,
        *,
        callbacks: DataverseDeleteAllFilesCallbacks = DataverseDeleteAllFilesCallbacks(),
    ) -> None:
        """
        Gets list of files from a Dataverse dataset and deletes all of them.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id164

        Args:
            dataverse_dataset (DataverseDatasetVersionObject): The Dataverse dataset of which the all files are to be deleted.
            callbacks (DataverDeleteAllFilesCallbacks): Optional request callbacks.
        """

        def _get_file_list_done(files: DataverseFileListObject):

            def _execute(session: requests.Session) -> DataverseDeleteAllFilesData:

                if files.ids:
                    resp = self.put(
                        session,
                        ["datasets", dataverse_dataset.dataset_id, "deleteFiles"],
                        json=files.ids,
                    )

                    return DataverseRequestData.data_from_response(
                        DataverseDeleteAllFilesData, resp
                    )
                else:
                    return DataverseDeleteAllFilesData(
                        data={"message": "No files to delete"}
                    )

            self._execute(
                cb_exec=_execute,
                cb_done=lambda data: callbacks.invoke_done_callbacks(
                    data=data, dataverse_dataset=dataverse_dataset
                ),
                cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
            )

        def _get_file_list_failed(exc: Exception):
            callbacks.invoke_fail_callbacks(exc)

        file_list_callbacks = DataverseGetFileListCallbacks()
        file_list_callbacks.done(_get_file_list_done)
        file_list_callbacks.failed(_get_file_list_failed)

        self.get_file_list(dataverse_dataset, callbacks=file_list_callbacks)

    def get_file_list(
        self,
        dataverse_dataset: DataverseDatasetVersionObject,
        *,
        callbacks: DataverseGetFileListCallbacks = DataverseGetFileListCallbacks(),
    ) -> None:
        """
        Retrieves the complete file list of a Dataverse dataset.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id86
        curl "$SERVER_URL/api/datasets/$ID/versions/$VERSION/files"

        Args:
            dataverse_dataset (DataverseDatasetVersionObject): The dataverse dataset of which the files are to be listed.
            callbacks (DataverseListAllFilesCallbacks): Optional request callbacks.
        """

        def _execute(session: requests.Session) -> DataverseFileListObject:
            resp = self.get(
                session,
                [
                    "datasets",
                    dataverse_dataset.dataset_id,
                    "versions",
                    ":draft",
                    "files",
                ],
            )

            return DataverseRequestData.data_from_response(
                DataverseFileListObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def upload_file(
        self,
        dataverse_dataset: DataverseDatasetObject,
        *,
        path: str,
        file_data: ResourceBuffer,
        callbacks: DataverseUploadFileCallbacks = DataverseUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to a Dataverse collection, creating any missing folders on the fly.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id107

        Args:
            dataverse_dataset (DataverseDatasetVersionObject): The dataverse dataset of which the files are to be listed.
            path (str): The remote path of the file.
            file_data (ResourcesBuffer): the file data.
            callbacks (DataverseUploadFileCallbacks): Optional request callbacks.
        """

        def _execute(session: requests.Session) -> DataverseFileObject:
            file_path = PurePosixPath(path)

            # When uploading, always seek to the beginning of the buffer, as uploads might be retried multiple times
            if file_data.seekable():
                file_data.seek(0)

            params_as_json_string = json.dumps(self._get_file_metadata(path))
            payload = dict(jsonData=params_as_json_string)

            # `requests` should set the `Content-Type` header implicitely to `multipart/form-data`
            # as per https://stackoverflow.com/a/35940980
            # this does not work when the `Content-Type` header is already present, which is why we delete it.
            del session.headers["Content-Type"]
            resp = self.post(
                session,
                ["datasets", dataverse_dataset.id, f"add"],
                files={
                    "file": (
                        file_path.name,
                        file_data.readall(),
                        "application/octet-stream",
                    )
                },
                data=payload,
            )

            return DataverseRequestData.data_from_response(DataverseFileObject, resp)

        def _upload_done(data: DataverseFileObject) -> None:
            callbacks.invoke_done_callbacks(data)
            file_data.close()  # Free up the buffer to save memory

        def _upload_failed(exc: Exception) -> None:
            callbacks.invoke_fail_callbacks(exc)
            file_data.close()  # Free up the buffer to save memory

        self._execute(
            cb_exec=_execute,
            cb_done=_upload_done,
            cb_failed=_upload_failed,
        )

    def delete_dataset_draft(
        self,
        dataverse_dataset: DataverseDatasetObject,
        *,
        callbacks: DataverseDeleteDatasetDraftCallbacks = DataverseDeleteDatasetDraftCallbacks(),
    ) -> None:
        """
        Deletes an existing Dataverse dataset draft. Only drafts can be deleted.
        Uses https://guides.dataverse.org/en/latest/api/native-api.html#id97

        Args:
            dataverse_dataset (DataverseDatasetObject): The Dataverse dataset to be deleted.
            callbacks (DataverseDeleteDatasetDraftCallbacks): Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            resp = self.delete(
                session, ["datasets", dataverse_dataset.id, "versions", ":draft"]
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def _customize_session(
        self,
        session: requests.Session,
        *,
        auth_strategy: AuthorizationStrategy | None,
        auth_token: AuthorizationToken | None,
    ):
        if auth_strategy and auth_token:
            session.headers.update(
                {
                    "X-Dataverse-key": auth_strategy.get_token_content(
                        auth_token, AuthorizationStrategy.ContentType.AUTH_TOKEN
                    )
                }
            )

    def _get_project_metadata(self, project: Project) -> dict:
        project_metadata = project.features.project_metadata.metadata
        shared_objects = project.features.shared_objects

        metadata = (
            DataverseMetadataBuilder()
            .with_title(project_metadata)
            .with_authors(project_metadata, shared_objects)
            .with_pocs(project_metadata, shared_objects)
            .with_description(project_metadata)
            .with_subject(project_metadata)
            .with_rights(project_metadata)
            .build()
        )

        return {
            "datasetVersion": {
                "license": dataclasses.asdict(metadata.rights),
                "metadataBlocks": {
                    "citation": {
                        "fields": [
                            {
                                "value": metadata.title,
                                "typeClass": "primitive",
                                "multiple": False,
                                "typeName": "title",
                            },
                            {
                                "value": [
                                    {
                                        "authorName": {
                                            "value": author.name,
                                            "typeClass": "primitive",
                                            "multiple": False,
                                            "typeName": "authorName",
                                        },
                                        "authorAffiliation": {
                                            "value": author.affiliation,
                                            "typeClass": "primitive",
                                            "multiple": False,
                                            "typeName": "authorAffiliation",
                                        },
                                    }
                                    for author in metadata.authors
                                ],
                                "typeClass": "compound",
                                "multiple": True,
                                "typeName": "author",
                            },
                            {
                                "value": [
                                    {
                                        "datasetContactEmail": {
                                            "typeClass": "primitive",
                                            "multiple": False,
                                            "typeName": "datasetContactEmail",
                                            "value": point_of_contact.email,
                                        },
                                        "datasetContactName": {
                                            "typeClass": "primitive",
                                            "multiple": False,
                                            "typeName": "datasetContactName",
                                            "value": point_of_contact.name,
                                        },
                                    }
                                    for point_of_contact in metadata.pocs
                                ],
                                "typeClass": "compound",
                                "multiple": True,
                                "typeName": "datasetContact",
                            },
                            {
                                "value": [
                                    {
                                        "dsDescriptionValue": {
                                            "value": metadata.description,
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "typeName": "dsDescriptionValue",
                                        }
                                    }
                                ],
                                "typeClass": "compound",
                                "multiple": True,
                                "typeName": "dsDescription",
                            },
                            {
                                "value": metadata.subject,
                                "typeClass": "controlledVocabulary",
                                "multiple": True,
                                "typeName": "subject",
                            },
                        ],
                        "displayName": "Citation Metadata",
                    }
                },
            }
        }

    def _get_file_metadata(self, path: str) -> dict:
        return dict(
            directoryLabel=pathlib.PurePosixPath(path).parent.name,
            categories=["Data"],
            restrict=False,
            tabIngest=False,
        )
