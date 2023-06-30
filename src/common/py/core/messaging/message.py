import abc
import dataclasses
import typing
import uuid
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .channel import Channel
from ...component import ComponentID

MessageName = str
Trace = uuid.UUID


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class Message(abc.ABC):
    name: MessageName
    
    origin: ComponentID
    sender: ComponentID
    target: Channel
    
    hops: typing.List[ComponentID] = field(default_factory=list)
    
    trace: Trace = field(default_factory=uuid.uuid4)
    
    @staticmethod
    def define(name: str):
        def decorator(cls):
            cls = dataclasses.dataclass(frozen=True, kw_only=True)(cls)  # Wrap the class in a dataclass
            __init__ = cls.__init__
            
            def __new_init__(self, *args, **kwargs):
                __init__(self, *args, name=MessageName(name), **kwargs)
            
            setattr(cls, "__init__", __new_init__)
            return cls
        
        return decorator


MessageType = typing.TypeVar("MessageType", bound=Message)
