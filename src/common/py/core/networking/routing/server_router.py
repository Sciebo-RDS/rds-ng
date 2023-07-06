from .network_router import NetworkRouter
from ...messaging import Message
from ...messaging.meta import MessageMetaInformation


class ServerRouter(NetworkRouter):
    def check_client_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        # We don't even run a client!
        return False
    
    def check_server_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        # Messages stemming from this component are sent to all clients except self
        return msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
