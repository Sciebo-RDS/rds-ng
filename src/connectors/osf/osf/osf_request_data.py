import typing

from common.py.utils import ExtendedDictionary, RequestData


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
        for error in self.data.value("errors", []):
            source = self.data.value_from_data(error, "source.pointer", "")
            detail = self.data.value_from_data(error, "detail", "Unknown error")
            errors.append(f"{source}: {detail}" if source != "" else detail)
        else:
            errors.append(self._response.reason)
        return "; ".join(errors)


class OSFObject(ExtendedDictionary):
    """
    Base for an OSF object.
    """

    def __init__(self, data: typing.Any, root: str = "data"):
        super().__init__(data)

        self._root = root

    def _get_data_path(self, path: str) -> str:
        return f"{self._root}.{path}" if self._root != "" else path


class OSFProjectObject(OSFObject):
    """
    OSF project object.
    """

    @property
    def project_id(self) -> str:
        """
        The ID  of the project.
        """
        return self.value(self._get_data_path("id"))

    @property
    def project_link(self) -> str:
        """
        The external link for the project.
        """
        return self.value(self._get_data_path("links.html"))


class OSFStorageObject(OSFObject):
    """
    OSF storage object.
    """

    def __init__(self, data: typing.Any):
        super().__init__(data)

        self._folders: typing.List[OSFStorageObject] = []

    @property
    def storage_id(self) -> str:
        """
        The ID of the storage.
        """
        return self.value(self._get_data_path("id"))

    @property
    def name(self) -> str:
        """
        The name (path) of the storage.
        """
        return self.value(self._get_data_path("attributes.name"))

    @property
    def is_public(self) -> bool:
        """
        Whether the project is public.
        """
        return self.value(self._get_data_path("attributes.public"))

    @property
    def file_link(self) -> str:
        """
        The link to upload files.
        """
        return self.value(self._get_data_path("links.upload"))

    @property
    def folder_link(self) -> str:
        """
        The link to create new folders.
        """
        return self.value(self._get_data_path("links.new_folder"))

    @property
    def folders(self) -> typing.List["OSFStorageObject"]:
        """
        A list of all sub-folders (as OSFStorageData).

        Notes:
            This list is initially empty and will only be filled as needed by the client.
        """
        return self._folders


class OSFFileObject(OSFObject):
    """
    OSF file object.
    """

    @property
    def delete_link(self) -> str:
        """
        The link to delete a file or folder.
        """
        return self.value(self._get_data_path("links.delete"))


class OSFFileListObject(OSFObject):
    """
    OSf file list object.
    """

    @property
    def files(self) -> typing.List[OSFFileObject]:
        """
        The list of files.
        """
        return [OSFFileObject(file_data, "") for file_data in self.value("data")]
