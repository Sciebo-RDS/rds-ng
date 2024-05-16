from .. import Verifier, VerificationException
from ...entities.project import Project
from ...entities.user import User


class ProjectVerifier(Verifier):
    """
    Verifies a project.
    """

    def __init__(self, project: Project, user: User):
        self._project = project
        self._user = user

    def verify_create(self) -> None:
        self._verify_id()
        self._verify_user_id()
        self._verify_title()
        self._verify_resource()

    def verify_update(self) -> None:
        self._verify_id()
        self._verify_user_id()
        self._verify_user_permissions()
        self._verify_title()
        self._verify_resource()

    def verify_delete(self) -> None:
        self._verify_id()
        self._verify_user_id()
        self._verify_user_permissions()

    def _verify_id(self) -> None:
        if self._project.project_id <= 0:
            raise VerificationException("Invalid project ID")

    def _verify_user_id(self) -> None:
        if self._project.user_id == "":
            raise VerificationException("Invalid user ID")

    def _verify_user_permissions(self) -> None:
        if self._project.user_id != self._user.user_id:
            raise VerificationException("Invalid project permissions")

    def _verify_title(self) -> None:
        if self._project.title == "":
            raise VerificationException("Missing project title")

    def _verify_resource(self) -> None:
        if self._project.resources_path == "":
            raise VerificationException("Missing project resources path")
