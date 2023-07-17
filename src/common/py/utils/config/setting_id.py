import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class SettingID:
    """
    A setting identifier.
    
    Settings are specified by a category they belong to, as well as their actual name.
    
    Categories support sub-categories by separating them using dots (`.`);
    when represented as a string, all component tokens are separated by dots.
    
    Attributes:
        category: The category name. Sub-categories can be separated by dots (`.`).
        name: The name of the setting.
    """
    category: str | None
    name: str
    
    def split(self) -> typing.List[str]:
        """
        Splits the entire identifier into single string tokens.
        
        Returns:
            The tokens list.
        """
        return str(self).split(".")
    
    def env_name(self, prefix: str) -> str:
        """
        Generates an environment variable name for this identifier.
        
        A setting identifier is translated to its corresponding environment variable name by replacing all dots (`.`) with underscores (`_`),
        prepending a `prefix`, as well as making everything uppercase.
    
        Args:
            prefix: The prefix to prepend.

        Returns:
            The corresponding environment variable name.
        """
        return f"{prefix}_{str(self).replace('.', '_')}".upper()
    
    def __str__(self) -> str:
        return f"{self.category}.{self.name}" if self.category is not None else self.name
    
    def __repr__(self) -> str:
        return str(self)
