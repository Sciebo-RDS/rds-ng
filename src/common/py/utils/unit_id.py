import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class UnitID:
    """
    A general unit identifier.
    
    A *unit* basically is something that has a unique identifier consisting of three parts: The general ``type`` (e.g., *'infra'* for components
    belonging to the overall infrastructure), the ``unit`` name itself (e.g., *'server'*), and an ``instance`` specifier (used to
    distinguish multiple instances of the same unit).
    
    Attributes:
        type: The unit type.
        unit: The unit name.
        instance: The instance specifier.
    """
    type: str
    unit: str
    instance: str | None = None
    
    def equals(self, other: typing.Self) -> bool:
        """
        Compares this identifier to another one.
        
        Args:
            other: The unit identifier to compare this one to.

        Notes:
            The ``instance`` specifiers are only compared if both are not ``None``.
            
        Returns:
            Whether both identifiers are equal.
        """
        if self.type != other.type or self.unit != other.unit:
            return False
        
        if self.instance is not None and other.instance is not None:
            if self.instance != other.instance:
                return False
        
        return True
    
    @staticmethod
    def from_string(id_str: str) -> 'UnitID':
        """
        Creates a new ``UnitID`` from a string.
        
        The string must be of the form ``<type>/<unit>/<instance>`` or ``<type>/<unit>``.
        
        Args:
            id_str: The unit identifier string.

        Returns:
            The newly created ``UnitID``.
            
        Raises:
            ValueError: If the passed string is invalid.
        """
        from pathlib import PurePosixPath
        path = PurePosixPath(id_str).parts
        if len(path) == 3:
            return UnitID(path[0], path[1], path[2])
        if len(path) == 2:
            return UnitID(path[0], path[1])
            
        raise ValueError(f"The unit ID '{id_str}' is invalid")
    
    def __str__(self) -> str:
        from pathlib import PurePosixPath
        path = PurePosixPath(self.type, self.unit, self.instance) if self.instance is not None else PurePosixPath(self.type, self.unit)
        return str(path)
