import typing
from http import HTTPStatus

import requests


class RequestData:
    """
    Class to easily access data from an HTTP request.
    """
    
    def __init__(self, resp: requests.Response):
        self._data = resp.json()
        self._is_erroneous = resp.status_code >= HTTPStatus.BAD_REQUEST

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
    def is_erroneous(self) -> bool:
        """
        Whether the response was erroneous.
        """
        return self._is_erroneous
