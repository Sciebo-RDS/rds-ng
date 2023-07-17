import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class SettingID:
    category: str | None
    name: str
    
    def split(self) -> typing.List[str]:
        return str(self).split(".")
    
    def env_name(self, prefix: str) -> str:
        return f"{prefix}_{str(self).replace('.', '_')}".upper()
    
    def __str__(self) -> str:
        return f"{self.category}.{self.name}" if self.category is not None else self.name
    
    def __repr__(self) -> str:
        return str(self)
