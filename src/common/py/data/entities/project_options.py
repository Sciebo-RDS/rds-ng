import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .entity_types import ProjectFeatureID, SnapInID


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectOptions:
    """
    Class holding all options of a **Project**.

    Attributes:
        optional_features: A list of all user-enabled optional features.
        optional_snapins: A list of all user-enabled optional UI snap-ins.
    """

    optional_features: typing.List[ProjectFeatureID] = field(default_factory=list)
    optional_snapins: typing.List[SnapInID] = field(default_factory=list)
