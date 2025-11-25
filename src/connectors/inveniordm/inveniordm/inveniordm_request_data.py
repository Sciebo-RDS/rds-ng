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
    def key(self) -> str:
        """
        The key of the file.
        """
        return str(self.value("key"))

    @property
    def file_id(self) -> str:
        """
        The ID of the file.
        """
        return str(self.value("file_id"))

    @property
    def content_link(self) -> str:
        """
        The content link of the file.
        """
        return str(self.value("links.content"))

    @property
    def commit_link(self) -> str:
        """
        The commit link of the file.
        """
        return str(self.value("links.commit"))


class InvenioRDMFileListObject(ExtendedDictionary):
    """
    InvenioRDM file list object.
    """

    def find_file(self, key: str) -> InvenioRDMFileObject | None:
        """
        Finds the file with the given key.

        Args:
            key: The key of the file.

        Returns:
            The found file or **None** otherwise.
        """
        for file in self.files:
            if file.key == key:
                return file
        else:
            return None

    @property
    def files(self) -> typing.List[InvenioRDMFileObject]:
        """
        The list of files.
        """
        return [InvenioRDMFileObject(file_data) for file_data in self.value("entries")]
