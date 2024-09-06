import typing

import requests

from common.py.utils import RequestData


class ZenodoRequestData(RequestData):
    """
    An HTTP response specific to the Zenodo API.
    """

    @property
    def error(self) -> str:
        """
        The error reason (in case the request failed).
        """
        if not self.is_erroneous:
            return ""

        err_msg = self.value("message", "Unknown error")
        errors: typing.List[str] = []
        for error in self.value("errors", []):
            field = self._value(error, "field", "")
            message = self._value(error, "message", "Unknown error")
            errors.append(f"{field}: {message}" if field != "" else message)
        else:
            errors.append(self._response.reason)
        return f"{err_msg} [{'; '.join(errors)}]"


class ZenodoProjectData(ZenodoRequestData):
    """
    Zenodo project data.
    """

    @property
    def project_id(self) -> str:
        """
        The ID  of the project.
        """
        return str(self.value("id"))


class ZenodoFileData(ZenodoRequestData):
    """
    Zenodo file data.
    """
