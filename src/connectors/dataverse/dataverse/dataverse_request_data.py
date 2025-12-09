import typing

from common.py.utils import ExtendedDictionary, RequestData


class DataverseRequestData(RequestData):
    """
    An HTTP response specific to the Dataverse API.
    """

    @property
    def error(self) -> str:
        """
        The error reason (in case the request failed)
        """
        if not self.is_erroneous:
            return ""

        errors: typing.List[str] = []

        # Check if we have a structured Dataverse error response
        if self.data is not None:
            status = self.data.value("status", "")
            code = self.data.value("code", "")
            message = self.data.value("message", "")
            request_url = self.data.value("requestUrl", "")
            request_method = self.data.value("requestMethod", "")

            # Build error message from available fields
            error_parts = []
            if status:
                error_parts.append(f"Status: {status}")
            if code:
                error_parts.append(f"Code: {code}")
            if message:
                error_parts.append(f"Message: {message}")
            if request_method and request_url:
                error_parts.append(f"Request: {request_method} {request_url}")

            if error_parts:
                errors.append("; ".join(error_parts))

        # Fallback to HTTP response reason if no structured error
        if not errors:
            errors.append(self._response.reason)

        return "; ".join(errors)


class DataverseObject(ExtendedDictionary):
    """
    Base for a Dataverse object.
    """

    def __init__(self, data: typing.Any, root: str = "data"):
        super().__init__(data)

        self._root = root

    def _get_data_path(self, path: str) -> str:
        return f"{self._root}.{path}" if self._root != "" else path


class DataverseUserObject(DataverseObject):
    """
    Dataverse user object.
    """

    @property
    def user_id(self) -> str:
        """
        The ID of the user.
        """
        return self.value(self._get_data_path("id"))

    @property
    def user_identifier(self) -> str:
        """
        The identifier of the user.
        """
        return self.value(self._get_data_path("identifier"))

    @property
    def user_display_name(self) -> str:
        """
        The display name of the user.
        """
        return self.value(self._get_data_path("displayName"))

    @property
    def user_first_name(self) -> str:
        """
        The first name of the user.
        """
        return self.value(self._get_data_path("firstName"))

    @property
    def user_last_name(self) -> str:
        """
        The last name of the user.
        """
        return self.value(self._get_data_path("lastName"))

    @property
    def user_email(self) -> str:
        """
        The email of the user.
        """
        return self.value(self._get_data_path("email"))

    @property
    def user_is_super_user(self) -> bool:
        """
        If the user is a superuser.
        """
        return self.value(self._get_data_path("superuser"))

    @property
    def user_deactivated(self) -> bool:
        """
        If the user is deativated.
        """
        return self.value(self._get_data_path("deactivated"))

    @property
    def user_persistent_user_id(self) -> str:
        """
        The persistent user id of the user
        """
        return self.value(self._get_data_path("persistentUserId"))


class DataverseCollectionObject(DataverseObject):
    """
    Dataverse collection object.
    """

    @property
    def id(self) -> str:
        """
        The ID of the Dataverse collection
        """
        return self.value(self._get_data_path("id"))

    @property
    def alias(self) -> str:
        """
        The alias of the Dataverse collection
        """
        return self.value(self._get_data_path("alias"))

    @property
    def name(self) -> str:
        """
        The name of the Dataverse collection
        """
        return self.value(self._get_data_path("name"))


class DataverseDatasetObject(DataverseObject):
    """
    Dataverse dataset object.
    """

    @property
    def id(self) -> str:
        return str(self.value(self._get_data_path("id")))

    @property
    def identifier(self) -> str:
        return self.value(self._get_data_path("identifier"))

    @property
    def persistent_url(self) -> str:
        return self.value(self._get_data_path("persistentUrl"))

    @property
    def persistent_id(self) -> str:
        return self.value(self._get_data_path("persistentId"))

    @property
    def protocol(self) -> str:
        return self.value(self._get_data_path("protocol"))

    @property
    def authority(self) -> str:
        return self.value(self._get_data_path("authority"))

    @property
    def separator(self) -> str:
        return self.value(self._get_data_path("separator"))

    @property
    def publisher(self) -> str:
        return self.value(self._get_data_path("publisher"))

    @property
    def publication_date(self) -> str:
        return self.value(self._get_data_path("publicationDate"))

    @property
    def storage_identifier(self) -> str:
        return self.value(self._get_data_path("storageIdentifier"))

    @property
    def dataset_type(self) -> str:
        return self.value(self._get_data_path("datasetType"))

    @property
    def latest_version(self) -> typing.Any:
        return self.value(self._get_data_path("latestVersion"))


class DataverseCreateDatasetObject(DataverseObject):
    """
    The response for a create dataset request.
    """

    @property
    def id(self) -> str:
        return str(self.value(self._get_data_path("id")))

    @property
    def persistent_id(self) -> str:
        return str(self.value(self._get_data_path("persistentId")))


class DataverseDatasetVersionObject(DataverseObject):
    """
    Dataverse dataset object for a specific version.
    """

    @property
    def id(self) -> str:
        return str(self.value(self._get_data_path("id")))

    @property
    def dataset_id(self) -> str:
        return str(self.value(self._get_data_path("datasetId")))


class DataverseFileObject(DataverseObject):
    pass


class DataverseFileMetadataRequest(DataverseObject):
    pass


class DataverseFileListObject(DataverseObject):
    """
    Holds the files of a Dataverse dataset
    """

    @property
    def ids(self) -> list:
        """
        Returns a list of all file IDs in the Dataverse dataset.
        """

        return [file["dataFile"]["id"] for file in self.value("data")]
