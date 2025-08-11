import json
import typing

from sqlalchemy import Text, TypeDecorator

ArrayValueType = typing.TypeVar("ArrayValueType")
DataclassType = typing.TypeVar("DataclassType")


class ArrayType(TypeDecorator, typing.Generic[ArrayValueType]):
    """
    Arbitrary array data type. This uses ; as default delimiter. Do not use if ; might appear in the data you are storing.
    """

    impl = Text

    cache_ok = True

    def __init__(
        self,
        *args,
        separator: str = ";",
        value_read: typing.Callable[[str], ArrayValueType] = str,
        value_write: typing.Callable[[ArrayValueType], str] = str,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._separator = separator
        self._value_read = value_read
        self._value_write = value_write

    def process_bind_param(self, value: typing.List[ArrayValueType], dialect) -> str:
        return self._separator.join(map(self._value_write, value))

    def process_result_value(
        self, value: str | None, dialect
    ) -> typing.List[ArrayValueType]:
        if value is None or value == "":
            return []

        return list(map(self._value_read, value.split(self._separator)))


class JSONEncodedDataType(TypeDecorator):
    """
    Generic JSON-encoded data.
    """

    impl = Text

    cache_ok = True

    def process_bind_param(self, value: typing.Any, dialect) -> str | None:
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value: str | None, dialect) -> typing.Any:
        return json.loads(value) if value is not None else None


class DataclassDataType(TypeDecorator, typing.Generic[DataclassType]):
    """
    Dataclass type.
    """

    impl = Text

    cache_ok = True

    def __init__(self, *args, dataclass_type: type[DataclassType], **kwargs):
        super().__init__(*args, **kwargs)

        self._dataclass_type = dataclass_type

    def process_bind_param(self, value: DataclassType, dialect) -> str:
        return value.to_json() if value is not None else None

    def process_result_value(self, value: str | None, dialect) -> DataclassType | None:
        return self._dataclass_type.schema().loads(value) if value is not None else None


class DataclassArrayType(TypeDecorator, typing.Generic[DataclassType]):
    """
    Dataclass array type. (De)Serializes arrays of dataclasses.
    Uses JSON to serialize Arrays to avoid having to use a delimiter that might appear in user input.
    """

    impl = Text

    cache_ok = True

    def __init__(self, *args, dataclass_type: type[DataclassType], **kwargs):

        super().__init__(*args, **kwargs)

        self._dataclass_type = dataclass_type

    def process_bind_param(self, value: typing.List[DataclassType], dialect) -> str:
        if not value:
            return ""

        return json.dumps({i: v.to_dict() for i, v in enumerate(value)})

    def process_result_value(
        self, value: str | None, dialect
    ) -> typing.List[DataclassType]:
        if not value:
            return []

        value = list(json.loads(value).values())

        return [self._dataclass_type.from_dict(i) for i in value]


class DataclassArrayDictType(TypeDecorator, typing.Generic[DataclassType]):
    """
    Dataclass array dict type. (De)Serializes dicts that have a string as key and arrays of dataclasses as values.

    e.g.
    ```json
    {
        "/Documents/Example.md": [
            { "id": "title", "value": { "title": "asd" }, "refs": [], "type": "" },
            { "id": "identifier", "value": {}, "refs": [], "type": "" },
            { "id": "description", "value": {}, "refs": [], "type": "" },
            {
            "id": "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/",
            "value": {},
            "refs": [],
            "type": ""
            }
        ]
    }
    ```

    """

    impl = Text

    cache_ok = True

    def __init__(self, *args, dataclass_type: type[DataclassType], **kwargs):

        super().__init__(*args, **kwargs)

        self._dataclass_type = dataclass_type

    def process_bind_param(
        self, value: typing.Dict[str, typing.List[DataclassType]], dialect
    ) -> str:
        if not value:
            return ""

        return json.dumps(
            {
                key: [v.to_dict() for _, v in enumerate(val)]
                for key, val in value.items()
            }
        )

    def process_result_value(
        self, value: str | None, dialect
    ) -> typing.Dict[str, DataclassType]:
        if not value:
            return {}

        parsed_json = json.loads(value)

        return {
            key: [self._dataclass_type.from_dict(e) for e in val]
            for key, val in parsed_json.items()
        }
