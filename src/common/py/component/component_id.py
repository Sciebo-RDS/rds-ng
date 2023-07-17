from dataclasses import dataclass

import typing


@dataclass(frozen=True)
class ComponentID:
    """
    A component identifier.
    
    Component identifiers consist of three parts: The general `type` (e.g., 'infra' for components belonging to the overall infrastructure),
    the `component` itself (e.g., 'gate' or 'server'), and an `instance` specifier (used to distinguish multiple instances of the same component).
    
    Attributes:
        type: The component type.
        component: The component name.
        instance: The instance specifier.
    """
    type: str
    component: str
    instance: str | None = None
    
    def equals(self, other: typing.Self) -> bool:
        """
        Compares this identifier to another one.
        
        Args:
            other: The component identifier to compare this one to.

        Notes:
            The `instance` specifiers are only compared if both are not ``None``.
            
        Returns:
            Whether both identifiers are equal.
        """
        if self.type != other.type or self.component != other.component:
            return False
        
        if self.instance is not None and other.instance is not None:
            if self.instance != other.instance:
                return False
        
        return True
    
    @staticmethod
    def from_string(s: str) -> 'ComponentID':
        """
        Creates a new :class:`ComponentID` from a string.
        
        The string must be of the form '<type>/<component>/<instance>' or '<type>/<component>'.
        
        Args:
            s: The component identifier string.

        Returns:
            The newly created :class:`ComponentID`.
            
        Raises:
            ValueError: If the passed string is invalid.
        """
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
