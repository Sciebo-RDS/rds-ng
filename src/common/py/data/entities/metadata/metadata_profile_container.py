from dataclasses import dataclass, field
from enum import StrEnum
from typing import List

from dataclasses_json import dataclass_json

from ..properties import ProfileMetadata, PropertyProfile


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

        Attributes:
            DEFAULT: A default (fixed) profile that will always be used.
            OPTIONAL: An optional profile.
        """

        DEFAULT = "default"
        OPTIONAL = "optional"

    category: str
    role: Role

    profile: PropertyProfile = field(
        default_factory=lambda: PropertyProfile(
            metadata=ProfileMetadata(("", ""), "", ""), layout=[]
        )
    )


MetadataProfileContainerList = List[MetadataProfileContainer]
