from dataclasses import dataclass
from enum import Flag, auto

import typing


@dataclass(frozen=True)
class ComponentID:
    """ A component ID consists of its overall type, the component name, and its running instance. """
    type: str
    component: str
    instance: str | None = None
    
    def equals(self, other: typing.Self) -> bool:
        if self.type != other.type or self.component != other.component:
            return False
        
        if self.instance is not None and other.instance is not None:
            if self.instance != other.instance:
                return False
        
        return True
    
    @staticmethod
    def from_string(s: str) -> 'ComponentID':
        from pathlib import PurePosixPath
        p = PurePosixPath(s).parts
        if len(p) == 3:
            return ComponentID(p[0], p[1], p[2])
        elif len(p) == 2:
            return ComponentID(p[0], p[1])
        else:
            raise ValueError(f"The component ID '{s}' is invalid")
    
    def __str__(self) -> str:
        from pathlib import PurePosixPath
        p = PurePosixPath(self.type, self.component, self.instance) if self.instance is not None else PurePosixPath(self.type, self.component)
        return str(p)
