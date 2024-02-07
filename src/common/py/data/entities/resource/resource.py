from dataclasses import dataclass
from enum import StrEnum

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class Resource:
    """
    A single file or folder resource.

    Attributes:
        filename: The complete name (path) of the resource.
        basename: The name (w/o path) of the resource.
        type: The type of the resource (folder or file).
        size: The size of the resource; for folders, this is the size of all its contents.
    """

    class Type(StrEnum):
        """
        The resource type.
        """

        FOLDER = "folder"
        FILE = "file"

    filename: str
    basename: str
    type: Type

    size: int = 0
