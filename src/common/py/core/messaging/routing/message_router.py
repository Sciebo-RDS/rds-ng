from .. import Message
from ..meta import MessageMetaInformation
from ....component import ComponentID


class MessageRouter:
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

    def check_local_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        if msg.target.is_local:
            return True
        elif msg.target.is_direct:
            # A direct message that has made it to the message bus either stems from this component or is targeted to it
            # If it is targeted to this component, it needs to be dispatched locally
            return msg.target.target_id.equals(self._comp_id)
        elif msg.target.is_room:
            # A room message is always dispatched locally if the component is subscribed to that room
            # TODO: Rooms: List of subscribed rooms, check if match -> local
            pass
        
        return False
    
    def check_remote_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        return not msg.target.is_local and msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
    
    def _verify_local_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        if msg_meta.entrypoint != MessageMetaInformation.Entrypoint.LOCAL:
            raise MessageRouter.RoutingError("Local message entering from a non-local location received")

    def _verify_direct_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        if msg.target.target_id is None:
            raise MessageRouter.RoutingError("Direct message without a target received")
        
        if msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL and msg.target.target_id.equals(self._comp_id):
            raise MessageRouter.RoutingError("Message coming from this component directed to self")
        elif msg_meta.entrypoint != MessageMetaInformation.Entrypoint.LOCAL and not msg.target.target_id.equals(self._comp_id):
            raise MessageRouter.RoutingError("Message coming from another component not directed to this component")

    def _verify_room_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        # Room messages must be targeted to a room
        if msg.target.target is None or msg.target.target == "":
            raise MessageRouter.RoutingError("Room message without a target room received")
        
        # Other than that, room messages are just ignored if they are sent to us even though we aren't subscribed to the room
