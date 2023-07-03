from .router_exception import RouterException
from .. import Message
from ....component import ComponentID


class MessageRouter:
    def __init__(self, comp_id: ComponentID):
        self._comp_id = comp_id
        
    def verify_message(self, msg: Message) -> None:
        if msg.target.is_direct:
            self._verify_direct_message(msg)
        elif msg.target.is_room:
            self._verify_room_message(msg)

    def check_local_routing(self, msg: Message) -> bool:
        if msg.target.is_local:
            return True
        elif msg.target.is_direct:
            return msg.target.target_id.equals(self._comp_id)
        elif msg.target.is_room:
            # TODO: Rooms: List of subscribed rooms, check if match -> local as well (maybe remote)
            pass
        
        return False

    def check_remote_routing(self, msg: Message) -> bool:
        if msg.target.is_local:
            return False
        elif msg.target.is_direct:
            return not msg.target.target_id.equals(self._comp_id)
        elif msg.target.is_room:
            # TODO: Rooms: List of subscribed rooms, check if match -> local as well (maybe remote)
            pass
        
        return False

    def _verify_direct_message(self, msg: Message) -> None:
        if msg.target.target_id is None:
            raise RouterException("Direct message without target received")
        
        if msg.origin.equals(self._comp_id) and msg.target.target_id.equals(self._comp_id):
            raise RouterException("Message coming from this component directed to self")

    def _verify_room_message(self, msg: Message) -> None:
        # TODO: !
        pass
