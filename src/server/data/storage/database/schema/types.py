import json
import typing

from sqlalchemy import TypeDecorator, Unicode

ArrayValueType = typing.TypeVar("ArrayValueType")


class ArrayType(TypeDecorator, typing.Generic[ArrayValueType]):
    """
    Arbitrary array data type.
    """

    impl = Unicode

    cache_ok = True

    def __init__(
        self,
        *args,
        separator: str = ";",
        value_conv: typing.Callable[[str], ArrayValueType] = str,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._separator = separator
        self._value_conv = value_conv

    def process_bind_param(self, value: typing.List[ArrayValueType], dialect) -> str:
        return self._separator.join(map(str, value))

    def process_result_value(
        self, value: str | None, dialect
    ) -> typing.List[ArrayValueType]:
        if value is None or value == "":
            return []

        return list(map(self._value_conv, value.split(self._separator)))


class JSONEncodedDataType(TypeDecorator):
    """
    Generic JSON-encoded data.
    """

    impl = Unicode

    cache_ok = True

    def process_bind_param(self, value: typing.Any, dialect) -> str | None:
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value: str | None, dialect) -> typing.Any:
        return json.loads(value) if value is not None else None
