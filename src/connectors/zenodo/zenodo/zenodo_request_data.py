import typing

from common.py.utils import ExtendedDictionary, RequestData


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

        err_msg = self.data.value("message", "Unknown error")
        errors: typing.List[str] = []
        for error in self.data.value("errors", []):
            field = self.data.value_from_data(error, "field", "")
            message = self.data.value_from_data(error, "message", "Unknown error")
            errors.append(f"{field}: {message}" if field != "" else message)
        else:
            errors.append(self._response.reason)
        return f"{err_msg} [{'; '.join(errors)}]"


class ZenodoProjectObject(ExtendedDictionary):
    """
    Zenodo project object.
    """

    @property
    def project_id(self) -> str:
        """
        The ID of the project.
        """
        return str(self.value("id"))

    @property
    def state(self) -> str:
        """
        The state of the project; can be *inprogress*, *done* or *error*.
        """
        return str(self.value("state"))

    @property
    def is_submitted(self) -> bool:
        """
        Whether the project has been submitted.
        """
        return bool(self.value("submitted"))

    @property
    def project_link(self) -> str:
        """
        The link to the project.
        """
        return str(self.value("links.html"))

    @property
    def bucket_link(self) -> str:
        """
        The link to the project.
        """
        return str(self.value("links.bucket"))


class ZenodoFileObject(ExtendedDictionary):
    """
    Zenodo file object.
    """

    @property
    def file_id(self) -> str:
        """
        The ID of the file.
        """
        return str(self.value("id"))


class ZenodoFileListObject(ExtendedDictionary):
    """
    Zenodo file list object.
    """

    @property
    def files(self) -> typing.List[ZenodoFileObject]:
        """
        The list of files.
        """
        return [ZenodoFileObject(file_data) for file_data in self._data]
