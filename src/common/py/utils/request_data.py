import typing
from http import HTTPStatus

import requests

from .extended_dictionary import ExtendedDictionary

DataType = typing.TypeVar("DataType", bound=ExtendedDictionary)


class RequestData:
    """
    Class to easily access data from an HTTP request.
    """
    
    def __init__(self, data_type: typing.Generic[DataType], resp: requests.Response, *, verify_response: bool = True):
        self._response = resp
        self._data = typing.cast(ExtendedDictionary, data_type(resp.json()))
        
        if verify_response:
            self._verify()
    
    def _verify(self) -> None:
        if self.is_erroneous:
            raise requests.RequestException(self.error, response=self._response)
        
    @property
    def data(self) -> DataType:
        """
        The data of the response.
        """
        return self._data
    
    @property
    def status_code(self) -> HTTPStatus:
        """
        The status code of the response.
        """
        return typing.cast(HTTPStatus, self._response.status_code)

    @property
    def is_erroneous(self) -> bool:
        """
        Whether the response was erroneous.
        """
        return self._response.status_code >= HTTPStatus.BAD_REQUEST
    
    @property
    def error(self) -> str:
        """
        The error reason (in case the request failed).
        """
        return self._response.reason if self.is_erroneous else ""
    
    @classmethod
    def from_response(cls, data_type: typing.Any, resp: requests.Response, *, verify_response: bool = True) -> "RequestData":
        """
        Creates a data response from an HTTP response.

        Args:
            data_type: The data type.
            resp: The HTTP response.
            verify_response: Whether to verify the response.

        Returns:
            The newly created request data.
        """
        return typing.cast(RequestData, cls(data_type, resp, verify_response=verify_response))
    
    @classmethod
    def data_from_response(cls, data_type: typing.Any, resp: requests.Response, *, verify_response: bool = True) -> DataType:
        """
        Creates a data response from an HTTP response and retrieves the data object.
        
        Args:
            data_type: The data type.
            resp: The HTTP response.
            verify_response: Whether to verify the response.

        Returns:
            The newly created data object.
        """
        return typing.cast(RequestData, cls(data_type, resp, verify_response=verify_response)).data

    def __str__(self) -> str:
        return f"{self._response}"
