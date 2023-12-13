import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .entity_types import ProjectFeatureID

UIOptions = typing.Dict[str, typing.Any]


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectOptions:
    """
    Class holding all options of a **Project**.

    Attributes:
        optional_features: A list of all user-enabled optional features.
        ui: Arbitrary UI options.
    """

    optional_features: typing.List[ProjectFeatureID] = field(default_factory=list)

    ui: UIOptions = field(default_factory=dict)
