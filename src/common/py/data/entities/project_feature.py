import abc
from dataclasses import dataclass

from dataclasses_json import dataclass_json

FeatureID = str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectFeature(abc.ABC):
    """
    Base data for a **Project** feature; specific features are derived from this class.

    A Project feature realizes the various aspects of a single project. Usually, a feature instance exists for each available feature to keep its data
    even if the feature itself is disabled for the project. If a feature is missing (e.g., it was added at a later time), the feature is considered disabled
    by default.

    Attributes:
        feature_id: The feature identifier.
        enabled: Whether the feature is enabled (activated) for the project.
    """

    feature_id: FeatureID

    enabled: bool
