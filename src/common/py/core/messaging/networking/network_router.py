from enum import IntEnum, auto

from .. import Message
from ..meta import MessageMetaInformation
from ....utils import UnitID


class NetworkRouter:
    """
    Network routing rules and logic.
    
    When a message enters the network engine in order to be sent to remote targets, it is first checked for its
    validity. Afterwards, the router decides through which channels (local, client, server) it needs to be sent.
    """
    class Direction(IntEnum):
        """
        Flag telling the direction (INcoming or OUTgoing) of a message.
        """
        IN = auto()
        OUT = auto()
        
    class RoutingError(RuntimeError):
        """
        Represents errors during routing validation.
        """
    
    def __init__(self, comp_id: UnitID, *, has_client: bool, has_server: bool):
        """
        Args:
            comp_id: The component id (required to decide whether we match a given direct target).
            has_client: Whether the network has a client instance.
            has_server: Whether the network has a server instance.
        """
        self._comp_id = comp_id
        
        self._has_client = has_client
        self._has_server = has_server
        
    def verify_message(self, direction: Direction, msg: Message) -> None:
        """
        Verifies whether a message may enter the network engine.
        
        Args:
            direction: The direction (*IN* or *OUT*) of the message.
            msg: The message that wants to enter the network engine.

        Raises:
            RoutingError: In case the message is not valid to enter the network engine.
        """
        if msg.target.is_local:
            self._verify_local_message(direction, msg)
        elif msg.target.is_direct:
            self._verify_direct_message(direction, msg)
        elif msg.target.is_room:
            self._verify_room_message(direction, msg)
            
    def check_local_routing(self, direction: Direction, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        """
        Checks if the message should be routed locally (dispatched via the message bus).
        
        Args:
            direction: The direction (*IN* or *OUT*) of the message.
            msg: The actual message.
            msg_meta: The message meta information.

        Returns:
            Whether local routing should happen.
        """
        if direction == NetworkRouter.Direction.OUT:
            return False  # Outgoing messages are never routed back locally
        if direction == NetworkRouter.Direction.IN:
            if msg.target.is_direct:
                return msg.target.target_id.equals(self._comp_id)
            
            return True
            
        return False
        
    def check_client_routing(self, direction: Direction, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        """
        Checks if the message should be routed through the client.

        Args:
            direction: The direction (*IN* or *OUT*) of the message.
            msg: The actual message.
            msg_meta: The message meta information.

        Returns:
            Whether client routing should happen.
        """
        if self._has_client:
            if direction == NetworkRouter.Direction.OUT:
                return True  # Always sent outgoing messages through the network
            if direction == NetworkRouter.Direction.IN:
                if msg.target.is_direct and msg.target.target_id.equals(self._comp_id):  # Skip messages targeted to us
                    return False
                
                return msg_meta.entrypoint == MessageMetaInformation.Entrypoint.SERVER  # Only rebounce to the client if the message came through the server
            
        return False
        
    def check_server_routing(self, direction: Direction, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        """
        Checks if the message should be routed through the server.

        Args:
            direction: The direction (*IN* or *OUT*) of the message.
            msg: The actual message.
            msg_meta: The message meta information.

        Returns:
            Whether server routing should happen.
        """
        if self._has_server:
            if direction == NetworkRouter.Direction.OUT:
                return True  # Always sent outgoing messages through the network
            if direction == NetworkRouter.Direction.IN:
                if msg.target.is_direct and msg.target.target_id.equals(self._comp_id):  # Skip messages targeted to us
                    return False
                
                return True  # Always send messages back through the server (the server will skip the original sender)
            
        return False
    
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
