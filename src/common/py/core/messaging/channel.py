from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class Channel:
    class Type(StrEnum):
        LOCAL = "local"
        DIRECT = "direct"
        ROOM = "room"
        
    type: Type
    target: str = None
    
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
