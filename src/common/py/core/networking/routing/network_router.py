import abc
import typing

from ...messaging import Message
from ...messaging.meta import MessageMetaInformation
from ....component import ComponentID


class NetworkRouter(abc.ABC):
    class RoutingError(RuntimeError):
        pass
    
    def __init__(self, comp_id: ComponentID):
        self._comp_id = comp_id
    
    def verify_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        if msg.target.is_local:
            self._verify_local_message(msg, msg_meta)
        if msg.target.is_direct:
            self._verify_direct_message(msg, msg_meta)
        elif msg.target.is_room:
            self._verify_room_message(msg, msg_meta)
            
    @abc.abstractmethod
    def check_client_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        return False
    
    @abc.abstractmethod
    def check_server_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> typing.Tuple[bool, typing.List[ComponentID]]:
        return False, []
 
    def _verify_local_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        # Local messages should never land here
        raise NetworkRouter.RoutingError("A local message was sent through the network engine")
    
    def _verify_direct_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        if msg.target.target_id is None:
            raise NetworkRouter.RoutingError("Direct message without a target sent")
    
    def _verify_room_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        # Room messages are just ignored if they are sent to us even though we aren't subscribed to the room
        # So there's nothing to verify here
        pass
