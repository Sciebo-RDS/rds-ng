from .network_router import NetworkRouter
from ...messaging import Message
from ...messaging.meta import MessageMetaInformation


class LeafRouter(NetworkRouter):
    def check_client_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        # Messages stemming from this component are always sent through the client
        return msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
    
    def check_server_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        # We don't even run a server!
        return False
