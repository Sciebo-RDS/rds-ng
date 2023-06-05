import abc
import typing
import uuid
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from .channel import Channel
from ...component import ComponentID

MessageName = PurePosixPath
Trace = uuid.UUID


@dataclass(frozen=True, kw_only=True)
class Message(abc.ABC):
    name: MessageName
    
    origin: ComponentID
    sender: ComponentID
    target: Channel
    
    hops: typing.List[ComponentID] = field(default_factory=list)
    
    trace: Trace = uuid.uuid4()


MessageType = typing.TypeVar("MessageType", bound=Message)
