from .verification_exception import VerificationException
from .verifier import Verifier
from ..entities.project import Project


class ProjectVerifier(Verifier):
    """
    Verifies a project.
    """

    def __init__(self, project: Project):
        self._project = project

    def verify_create(self) -> None:
        self._verify_id()
        self._verify_title()

    def verify_update(self) -> None:
        self._verify_id()
        self._verify_title()

    def verify_delete(self) -> None:
        self._verify_id()

    def _verify_id(self) -> None:
        if self._project.project_id <= 0:
            raise VerificationException("Invalid project ID")

    def _verify_title(self) -> None:
        if self._project.title == "":
            raise VerificationException("Missing project title")
