import abc
from enum import IntEnum, auto

from ... import Message
from ...meta import MessageMetaInformation
from .....component import ComponentID


class NetworkRouter(abc.ABC):
    class Direction(IntEnum):
        IN = auto()
        OUT = auto()
        
    class RoutingError(RuntimeError):
        pass
    
    def __init__(self, comp_id: ComponentID, *, has_client: bool, has_server: bool):
        self._comp_id = comp_id
        
        self._has_client = has_client
        self._has_server = has_server
        
    def verify_message(self, direction: Direction, msg: Message) -> None:
        if msg.target.is_local:
            self._verify_local_message(direction, msg)
        if msg.target.is_direct:
            self._verify_direct_message(direction, msg)
        elif msg.target.is_room:
            self._verify_room_message(direction, msg)
            
    def check_local_routing(self, direction: Direction, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        if direction == NetworkRouter.Direction.OUT:
            return False  # Outgoing messages are never routed back locally
        elif direction == NetworkRouter.Direction.IN:
            if msg.target.is_direct:
                return msg.target.target_id.equals(self._comp_id)
            elif msg.target.is_room:
                return True
            
        return False
        
    def check_client_routing(self, direction: Direction, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        if direction == NetworkRouter.Direction.OUT:
            return self._has_client
        else:
            return False  # TODO
        
    def check_server_routing(self, direction: Direction, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        if direction == NetworkRouter.Direction.OUT:
            return self._has_server
        else:
            return False  # TODO
    
    def _verify_local_message(self, direction: Direction, msg: Message) -> None:
        # Local messages should never land here
        raise NetworkRouter.RoutingError("A local message was directed to the network engine")
    
    def _verify_direct_message(self, direction: Direction, msg: Message) -> None:
        # An incoming direct message must be targeted to a component
        if msg.target.target_id is None:
            raise NetworkRouter.RoutingError("Direct message without a target received")
        
        # Outgoing direct messages may not be directed to this component
        if direction == NetworkRouter.Direction.OUT:
            if msg.target.target_id.equals(self._comp_id):
                raise NetworkRouter.RoutingError("Direct message to this component sent through the network engine")
    
    def _verify_room_message(self, direction: Direction, msg: Message) -> None:
        # Room messages must be targeted to a room
        if msg.target.target is None or msg.target.target == "":
            raise NetworkRouter.RoutingError("Room message without a target room received")
