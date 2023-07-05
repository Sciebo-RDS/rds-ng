from .. import Message
from ....component import ComponentID


class MessageRouter:
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

    def check_local_routing(self, msg: Message) -> bool:
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
    
    def check_remote_routing(self, msg: Message) -> bool:
        if msg.target.is_local:
            return False
        elif msg.target.is_direct:
            # A direct message that has made it to the message bus either stems from this component or is targeted to it
            # If it is not targeted to this component, it needs to be dispatched remotely
            return not msg.target.target_id.equals(self._comp_id)
        elif msg.target.is_room:
            # Room messages are always dispatched remotely (but messages will never "bounce back" to their origin)
            # The actual logic of remote dispatching is handled by the NWE (which might result in not dispatching them remotely)
            # TODO: Never bounce a room msg that comes through the client back through the client (NWE)
            return True
        
        return False
    
    def _verify_local_message(self, msg: Message) -> None:
        # Nothing to verify here
        pass

    def _verify_direct_message(self, msg: Message) -> None:
        if msg.target.target_id is None:
            raise MessageRouter.RoutingError("Direct message without a target received")
        
        if msg.origin.equals(self._comp_id) and msg.target.target_id.equals(self._comp_id):
            raise MessageRouter.RoutingError("Message coming from this component directed to self")
        elif not msg.origin.equals(self._comp_id) and not msg.target.target_id.equals(self._comp_id):
            raise MessageRouter.RoutingError("Message coming from another component not directed to this component")

    def _verify_room_message(self, msg: Message) -> None:
        # Room messages are just ignored if they are sent to us even though we aren't subscribed to the room
        # So there's nothing to verify here
        pass
