import abc
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class SnapIn(abc.ABC):
    """
    Base data class for a project feature.
    """
