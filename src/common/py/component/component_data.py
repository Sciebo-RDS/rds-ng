import dataclasses

from semantic_version import Version

from .component_id import ComponentID
from .roles.component_role import ComponentRole
from ..utils.config import Configuration


@dataclasses.dataclass(frozen=True, kw_only=True)
class ComponentData:
    comp_id: ComponentID
    role: ComponentRole
    
    config: Configuration
    
    title: str
    name: str
    version: Version
