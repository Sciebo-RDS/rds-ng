from .network_router import NetworkRouter
from ...messaging import Message


class LeafRouter(NetworkRouter):
    def check_client_routing(self, msg: Message) -> bool:
        # Messages that stem from this component and are targeted for another component are always sent through the client
        return msg.origin.equals(self._comp_id) and (msg.target.target_id is not None and not msg.target.target_id.equals(self._comp_id))
    
    def check_server_routing(self, msg: Message) -> bool:
        # We don't even run a server!
        return False
