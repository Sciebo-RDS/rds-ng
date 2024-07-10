import typing

from common.py.utils import RequestData


class OSFRequestData(RequestData):
    """
    An HTTP response specific to the OSF API.
    """

    @property
    def error(self) -> str:
        """
        The error reason (in case the request failed).
        """
        if not self.is_erroneous:
            return ""

        errors: typing.List[str] = []
        for error in self.value("errors", []):
            source = self._value(error, "source.pointer", "")
            detail = self._value(error, "detail", "Unknown error")
            errors.append(f"{source}: {detail}" if source != "" else detail)
        return "; ".join(errors)


class OSFCreateProjectData(OSFRequestData):
    """
    Data from a `create_project` API call.
    """

    @property
    def project_id(self) -> str:
        """
        The ID (within OSF) of the project.
        """
        return self.value("data.id")
