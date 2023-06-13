import typing

from ...core.messaging import MessageBusProtocol, Message, MessageType, Channel
from ...component import ComponentID


class MessageEmitter:
    """ A helper class to create and emit messages; it basically stores senseful defaults for certain values and takes care of chaining and rerouting. """
    def __init__(self, origin_id: ComponentID, message_bus: MessageBusProtocol):
        self._origin_id = origin_id
        self._message_bus = message_bus
        
    def emit(self, msg_type: typing.Type[MessageType], target: Channel, chain: Message | None = None, **kwargs) -> MessageType:
        return self._emit(msg_type, origin=self._origin_id, target=target, prev_hops=[], chain=chain, **kwargs)
    
    def _emit(self, msg_type: typing.Type[MessageType], *, origin: ComponentID, target: Channel, prev_hops: typing.List[ComponentID], chain: Message | None, **kwargs) -> MessageType:
        msg = self._create(msg_type, origin=origin, target=target, prev_hops=prev_hops, chain=chain, **kwargs)
        self._message_bus.dispatch(msg)
        return msg

    def _create(self, msg_type: typing.Type[MessageType], *, origin: ComponentID, target: Channel, prev_hops: typing.List[ComponentID], chain: Message | None, **kwargs) -> MessageType:
        if chain is not None:
            kwargs["trace"] = chain.trace
        
        return msg_type(origin=origin, sender=self._origin_id, target=target, hops=[*prev_hops, self._origin_id], **kwargs)
