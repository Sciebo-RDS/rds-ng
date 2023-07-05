import abc
import typing

from ...messaging import Message
from ....component import ComponentID


class NetworkRouter(abc.ABC):
    class RoutingError(RuntimeError):
        pass
    
    def __init__(self, comp_id: ComponentID):
        self._comp_id = comp_id
    
    def verify_message(self, msg: Message) -> None:
        if msg.target.is_local:
            self._verify_local_message(msg)
        if msg.target.is_direct:
            self._verify_direct_message(msg)
        elif msg.target.is_room:
            self._verify_room_message(msg)
            
    @abc.abstractmethod
    def check_client_routing(self, msg: Message) -> bool:
        return False
    
    @abc.abstractmethod
    def check_server_routing(self, msg: Message) -> typing.Tuple[bool, typing.List[ComponentID]]:
        return False, []
 
    def _verify_local_message(self, msg: Message) -> None:
        # Local messages should never land here
        raise NetworkRouter.RoutingError("A local message was sent through the network engine")
    
    def _verify_direct_message(self, msg: Message) -> None:
        if msg.target.target_id is None:
            raise NetworkRouter.RoutingError("Direct message without a target sent")
    
    def _verify_room_message(self, msg: Message) -> None:
        # Room messages are just ignored if they are sent to us even though we aren't subscribed to the room
        # So there's nothing to verify here
        pass
