from dataclasses import dataclass
from enum import StrEnum

from ...utils import UnitID


@dataclass(frozen=True)
class Channel:
    """
    The target of a message.
    
    Message targets are represented by so-called *channels*. These can be *local* for messages that will only
    be dispatched locally and not across the network, *direct* for specific (remote) targets, as well as general
    *rooms* consisting of arbitrary participants (this is still WIP and may even be removed later).
    
    Attributes:
        type: The channel type.
        target: The actual target (either a direct one or a room).
    """
    class Type(StrEnum):
        """
        The different channel types.
        """
        LOCAL = "local"
        DIRECT = "direct"
        ROOM = "room"
        
    type: Type
    target: str | None = None
    
    @property
    def target_id(self) -> UnitID | None:
        """
        Generates a ``UnitID`` from the target of this channel.
        
        Returns:
            The component ID of the target, if any.
        """
        try:
            return UnitID.from_string(self.target) if self.target is not None else None
        except:  # pylint: disable=bare-except
            return None
    
    @property
    def is_local(self) -> bool:
        """
        Whether this is a local channel.
        """
        return self.type == Channel.Type.LOCAL
    
    @property
    def is_direct(self) -> bool:
        """
        Whether this is a direct channel.
        """
        return self.type == Channel.Type.DIRECT
    
    @property
    def is_room(self) -> bool:
        """
        Whether this is a room channel.
        """
        return self.type == Channel.Type.ROOM
    
    def __str__(self) -> str:
        return f"@{self.type}:{self.target}" if self.target is not None else f"@{self.type}"
    
    @staticmethod
    def local() -> 'Channel':
        """
        Creates a new local channel.
        """
        return Channel(Channel.Type.LOCAL)
        
    @staticmethod
    def direct(target: str) -> 'Channel':
        """
        Creates a new direct channel.
        """
        return Channel(Channel.Type.DIRECT, target)
    
    @staticmethod
    def room(target: str) -> 'Channel':
        """
        Creates a new room channel.
        """
        return Channel(Channel.Type.ROOM, target)
