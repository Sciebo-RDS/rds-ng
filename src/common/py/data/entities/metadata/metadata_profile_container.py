from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Dict, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class MetadataProfileContainer:
    """
    A container that holds a metadata profile along with various descriptive information.

    Attributes:
        category: The overall category of the profile.
        role: The role of the profile within its category.
        profile: The actual profile data.
    """

    class Role(StrEnum):
        """
        The role of a profile.
        """

        TEMPLATE = "template"
        GLOBAL = "global"

    category: str
    role: Role

    profile: Dict[str, Dict[str, Any]] = field(
        default_factory=dict
    )  # TODO: Proper type


MetadataProfileContainerList = List[MetadataProfileContainer]
