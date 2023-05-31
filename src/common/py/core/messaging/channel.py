import typing
from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class Channel:
    class Type(StrEnum):
        LOCAL = "local"
        GLOBAL = "global"
        DIRECT = "direct"
        ROOM = "room"
        
    type: Type
    target: str = None
    
    def __str__(self) -> str:
        return f"@{self.type}:{self.target}" if self.target is not None else f"@{self.type}"


def local_channel() -> Channel:
    return Channel(Channel.Type.LOCAL)


def global_channel() -> Channel:
    return Channel(Channel.Type.GLOBAL)


def direct_channel(target: str) -> Channel:
    return Channel(Channel.Type.DIRECT, target)


def room_channel(target: str) -> Channel:
    return Channel(Channel.Type.ROOM, target)
