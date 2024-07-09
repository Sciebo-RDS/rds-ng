import typing

from common.py.utils import RequestData


class OSFRequestData(RequestData):
    """
    An HTTP response specific to the OSF API.
    """

    @property
    def errors(self) -> typing.List[str]:
        """
        A list of all errors found in the response.
        """
        if not self.is_erroneous:
            return []

        errors: typing.List[str] = []
        for error in self.value("errors", []):
            source = self._value(error, "source.pointer", "")
            detail = self._value(error, "detail", "Unknown error")
            errors.append(f"{source}: {detail}" if source != "" else detail)
        return errors
