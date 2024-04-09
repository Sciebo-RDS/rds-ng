import json
import typing

from sqlalchemy import TypeDecorator, Unicode


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
