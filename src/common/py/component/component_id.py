from dataclasses import dataclass
from enum import Flag, auto

import typing


@dataclass(frozen=True)
class ComponentID:
    """ A component ID consists of its overall type, the component name, and its running instance. """
    class Tokens(Flag):
        TYPE = auto()
        COMPONENT = auto()
        INSTANCE = auto()
        ALL = TYPE | COMPONENT | INSTANCE
    
    type: str
    component: str
    instance: str = "default"
    
    def partial_eq(self, other: typing.Self, tokens: Tokens = Tokens.ALL) -> bool:
        if ComponentID.Tokens.TYPE in tokens and self.type != other.type:
            return False
        
        if ComponentID.Tokens.COMPONENT in tokens and self.component != other.component:
            return False
        
        if ComponentID.Tokens.INSTANCE in tokens and self.instance != other.instance:
            return False
        
        return True
    
    def __str__(self) -> str:
        from pathlib import PurePosixPath
        p = PurePosixPath(self.type, self.component, self.instance)
        return str(p)

    @staticmethod
    def from_string(s: str) -> 'ComponentID':
        from pathlib import PurePosixPath
        p = PurePosixPath(s).parts
        if len(p) != 3:
            raise ValueError(f"The component ID '{s}' is invalid")
        return ComponentID(p[0], p[1], p[2])
