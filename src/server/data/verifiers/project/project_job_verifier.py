import json

from common.py.data.entities.connector import Connector
from common.py.data.entities.metadata import filter_containers, MetadataProfileContainer
from common.py.data.entities.project import Project, ProjectJob
from common.py.data.entities.project.features import ProjectMetadataFeature
from common.py.data.metadata import MetadataParser
from common.py.data.verifiers import VerificationException, Verifier


class ProjectJobVerifier(Verifier):
    """
    Verifies a project job.
    """

    def __init__(self, project: Project, job: ProjectJob, connector: Connector):
        self._project = project
        self._job = job
        self._connector = connector

    def verify_create(self) -> None:
        self._verify_job()
        self._verify_metadata()

    def verify_update(self) -> None:
        self._verify_job()
        self._verify_metadata()

    def verify_delete(self) -> None:
        self._verify_job()

    def _verify_job(self) -> None:
        if self._job.project_id <= 0:
            raise VerificationException("Invalid project job ID")
        if self._job.user_id == "":
            raise VerificationException("Invalid user ID")
        if self._job.connector_instance == "":
            raise VerificationException("Invalid connector instance")

    def _verify_metadata(self) -> None:
        from ....component import ServerComponent

        # Verify all global metadata profiles
        profiles = filter_containers(
            ServerComponent.instance().server_data.profile_containers,
            category=ProjectMetadataFeature.feature_id,
            role=MetadataProfileContainer.Role.GLOBAL,
        )

        for profile in profiles:
            MetadataParser.validate_metadata(
                profile.profile,
                self._project.features.project_metadata.metadata,
                self._project.features.project_metadata.shared_objects,
            )

        # Verify the connector profile
        MetadataParser.validate_metadata(
            self._connector.metadata_profile,
            self._project.features.project_metadata.metadata,
            self._project.features.project_metadata.shared_objects,
        )
