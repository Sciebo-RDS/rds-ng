import typing
from http import HTTPStatus

import requests


class RequestData:
    """
    Class to easily access data from an HTTP request.
    """
    
    def __init__(self, resp: requests.Response, *, verify_response: bool = True):
        self._response = resp
        self._data = resp.json()
        
        if verify_response:
            self._verify()
    
    def _verify(self) -> None:
        if self.is_erroneous:
            raise RuntimeError(self.error)
    
    def value(self, path: str, default: typing.Any = None) -> typing.Any:
        """
        Gets a value from the response, supporting dot notation.
        
        Args:
            path: The full value path.
            default: A default value.

        Returns:
            The value or the default one if none was found.
        """
        return self._value(self._data, path, default)

    def _value(
        self, data: typing.Any, path: str, default: typing.Any = None
    ) -> typing.Any:
        value = data
        try:
            for key in path.split("."):
                value = value[key]
            return value
        except KeyError:
            return default
        
    @property
    def data(self) -> typing.Any:
        """
        The raw response data.
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
