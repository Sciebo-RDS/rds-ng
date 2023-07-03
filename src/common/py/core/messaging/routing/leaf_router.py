from .message_router import MessageRouter
from .router_exception import RouterException
from .. import Message


class LeafRouter(MessageRouter):
    def _verify_direct_message(self, msg: Message) -> None:
        super()._verify_direct_message(msg)
        
        if not msg.origin.equals(self._comp_id) and not msg.target.target_id.equals(self._comp_id):
            raise RouterException("Message coming from another component not directed to this component")
