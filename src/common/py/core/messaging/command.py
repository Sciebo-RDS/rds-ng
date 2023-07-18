import typing
import uuid
from dataclasses import dataclass, field

from .message import Message, Trace


@dataclass(frozen=True, kw_only=True)
class Command(Message):
    """
    A command message.
    
    Commands are instructions that need to be 'executed' by the receiving component.
    
    Notes:
          Commands need to `always` be replied by emitting a corresponding :class:`CommandReply`.
          This reply is then automatically sent back to the original sender.
    
    Attributes:
        unique: A unique identifier for each issued command.
    """
    unique: Trace = field(default_factory=uuid.uuid4)


CommandType = typing.TypeVar("CommandType", bound=Command)
