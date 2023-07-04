from dataclasses import dataclass
from enum import StrEnum

from ...component import ComponentID


@dataclass(frozen=True)
class Channel:
    class Type(StrEnum):
        LOCAL = "local"
        DIRECT = "direct"
        ROOM = "room"
        
    type: Type
    target: str | None = None
    
    @property
    def target_id(self) -> ComponentID | None:
        try:
            return ComponentID.from_string(self.target) if self.target is not None else None
        except:
            return None
    
    @property
    def is_local(self) -> bool:
        return self.type == Channel.Type.LOCAL
    
    @property
    def is_direct(self) -> bool:
        return self.type == Channel.Type.DIRECT
    
    @property
    def is_room(self) -> bool:
        return self.type == Channel.Type.ROOM
    
    def __str__(self) -> str:
        return f"@{self.type}:{self.target}" if self.target is not None else f"@{self.type}"
    
    @staticmethod
    def local() -> 'Channel':
        return Channel(Channel.Type.LOCAL)
        
    @staticmethod
    def direct(target: str) -> 'Channel':
        return Channel(Channel.Type.DIRECT, target)
    
    @staticmethod
    def room(target: str) -> 'Channel':
        return Channel(Channel.Type.ROOM, target)
