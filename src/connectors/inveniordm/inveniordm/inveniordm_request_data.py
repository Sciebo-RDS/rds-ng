import typing

from common.py.utils import ExtendedDictionary, RequestData


class InvenioRDMRequestData(RequestData):
    """
    An HTTP response specific to the InvenioRDM API.
    """

    @property
    def error(self) -> str:
        """
        The error reason (in case the request failed).
        """
        if not self.is_erroneous:
            return ""

        err_msg = self.data.value("message", "Unknown error")
        return err_msg


class InvenioRDMProjectObject(ExtendedDictionary):
    """
    InvenioRDM project object.
    """

    @property
    def project_id(self) -> str:
        """
        The ID of the project.
        """
        return str(self.value("id"))

    @property
    def is_published(self) -> bool:
        """
        Whether the project has been published.
        """
        return bool(self.value("is_published"))

    @property
    def project_link(self) -> str:
        """
        The link to the project.
        """
        return str(self.value("links.self_html"))


class InvenioRDMFileObject(ExtendedDictionary):
    """
    InvenioRDM file object.
    """

    @property
    def file_id(self) -> str:
        """
        The ID of the file.
        """
        return str(self.value("id"))


class InvenioRDMFileListObject(ExtendedDictionary):
    """
    InvenioRDM file list object.
    """

    @property
    def files(self) -> typing.List[InvenioRDMFileObject]:
        """
        The list of files.
        """
        return [InvenioRDMFileObject(file_data) for file_data in self._data]
