import abc
import typing
import uuid
from dataclasses import dataclass

from . import Channel
from . import MessageName
from ...component import ComponentID

Trace = uuid.UUID


@dataclass(frozen=True, kw_only=True)
class Message(abc.ABC):
    name: MessageName
    
    origin: ComponentID
    sender: ComponentID
    target: Channel
    
    hops: typing.List[ComponentID]
    
    trace: Trace
