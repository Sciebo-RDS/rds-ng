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


class OSFProjectData(OSFRequestData):
    """
    OSF project data.
    """

    @property
    def project_id(self) -> str:
        """
        The ID  of the project.
        """
        return self.value("data.id")


class OSFStorageData(OSFRequestData):
    """
    OSF storage data.
    """

    @property
    def storage_id(self) -> str:
        """
        The ID of the storage.
        """
        return self.value("data.id")

    @property
    def file_link(self) -> str:
        """
        The link to upload files.
        """
        return self.value("data.links.upload")

    @property
    def folder_link(self) -> str:
        """
        The link to create new folders.
        """
        return self.value("data.links.new_folder")
