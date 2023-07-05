from ...messaging import Message
from ....component import ComponentID


class NetworkRouter:
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
            
    def check_client_routing(self, msg: Message) -> bool:
        return False
    
    def check_server_routing(self, msg: Message) -> bool:
        return False
 
    def _verify_local_message(self, msg: Message) -> None:
        # Local messages should never land here
        raise NetworkRouter.RoutingError("A local message was sent through the network engine")
    
    def _verify_direct_message(self, msg: Message) -> None:
        # TODO
        pass
    
    def _verify_room_message(self, msg: Message) -> None:
        # TODO
        pass
