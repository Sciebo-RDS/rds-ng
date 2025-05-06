import typing


class ExtendedDictionary:
    """
    Class to access data from a dictionary through dot notation.
    """
    
    def __init__(self, data: typing.Any):
        self._data = data
        
    def value(self, path: str, default: typing.Any = None) -> typing.Any:
        """
        Gets a value from the dictionary, supporting dot notation.
        
        Args:
            path: The full value path.
            default: A default value.

        Returns:
            The value or the default one if none was found.
        """
        return self.value_from_data(self._data, path, default)

    def value_from_data(
        self, data: typing.Any, path: str, default: typing.Any = None
    ) -> typing.Any:
        """
        Gets a value from a specific data object.
        
        Args:
            data: The data object.
            path: The value path.
            default: A default value.

        Returns:
            The value or the default one if none was found.
        """
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
        The raw data.
        """
        return self._data
    
    def __str__(self) -> str:
        return f"{self.data}"
