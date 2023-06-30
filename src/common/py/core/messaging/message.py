import abc
import dataclasses
import typing
import uuid
from dataclasses import dataclass, field

from .channel import Channel
from ...component import ComponentID

MessageName = str
Trace = str


@dataclass(frozen=True, kw_only=True)
class Message(abc.ABC):
    name: MessageName
    
    origin: ComponentID
    sender: ComponentID
    target: Channel
    
    hops: typing.List[ComponentID] = field(default_factory=list)
    
    trace: Trace = field(default_factory=lambda: str(uuid.uuid4()))
    
    def data(self) -> typing.Dict[typing.Any, typing.Any]:
        return dataclasses.asdict(self)
    
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
