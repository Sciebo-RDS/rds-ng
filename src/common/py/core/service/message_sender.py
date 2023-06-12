import typing

from ...core.messaging.message import MessageType
from ...core.messaging.channel import Channel
from ...component import ComponentID


class MessageSender:
    """ A helper class to create and send messages; it basically stores senseful defaults for certain values and takes care of chaining and rerouting. """
    def __init__(self, origin_id: ComponentID):
        self._origin_id = origin_id
        
    def create(self, msg_type: typing.Type[MessageType], target: Channel, **kwargs) -> MessageType:
        return self._create(msg_type, origin=self._origin_id, target=target, prev_hops=[], **kwargs)
    
    def _create(self, msg_type: typing.Type[MessageType], *, origin: ComponentID, target: Channel, prev_hops: typing.List[ComponentID], **kwargs) -> MessageType:
        return msg_type(origin=origin, sender=self._origin_id, target=target, hops=[*prev_hops, self._origin_id], **kwargs)
