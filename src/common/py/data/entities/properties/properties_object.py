from dataclasses import dataclass
from typing import Any, List

from dataclasses_json import DataClassJsonMixin

PropertyValues = dict[str, Any]

@dataclass
class PropertyObject(DataClassJsonMixin):
    """
    A project object.

    Attributes:
        id: The ID of the object.
        value: The values of the object.
        refs: The references that the object holds to other objects, by their id.
    """

    id: str
    value: PropertyValues
    refs: List[str]
    type: str = ""