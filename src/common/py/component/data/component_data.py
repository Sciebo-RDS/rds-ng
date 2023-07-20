import dataclasses

from semantic_version import Version

from .component_id import ComponentID
from ..roles.component_role import ComponentRole
from ...utils.config import Configuration


@dataclasses.dataclass(frozen=True, kw_only=True)
class ComponentData:
    """
    Holds general data and information about the component.
    
    Objects of this class are passed to certain parts of the core for easy access to frequently
    used component information and data, like its configuration or role.
    
    Attributes:
        comp_id: The component identifier.
        role: The component role.
        config: The configuration.
        title: The project title.
        name: The component name.
        version: The project version.
    """
    comp_id: ComponentID
    role: ComponentRole
    
    config: Configuration
    
    title: str
    name: str
    version: Version
