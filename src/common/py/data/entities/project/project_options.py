import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .features import ProjectFeatureID
from ..connector import ConnectorInstanceID

UIOptions = typing.Dict[str, typing.Any]


@dataclass_json
@dataclass(kw_only=True)
class ProjectOptions:
    """
    Class holding all options of a **Project**.

    Attributes:
        optional_features: A list of all user-enabled optional features.
        use_all_connector_instances: Whether all available connector instances should be used.
        active_connector_instances: List of connector instances to use for the project (if *use_all_connector_instances* is false).
        ui: Arbitrary UI options.
    """

    optional_features: typing.List[ProjectFeatureID] = field(default_factory=list)

    use_all_connector_instances: bool = True
    active_connector_instances: typing.List[ConnectorInstanceID] = field(
        default_factory=list
    )

    ui: UIOptions = field(default_factory=dict)
