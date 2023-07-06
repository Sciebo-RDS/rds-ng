from .network_router import NetworkRouter
from ...messaging import Message
from ...messaging.meta import MessageMetaInformation


class NodeRouter(NetworkRouter):
    def check_client_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        # Messages stemming from this component go out to the server
        return msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
    
    def check_server_routing(self, msg: Message, msg_meta: MessageMetaInformation) -> bool:
        # Messages stemming from this component are sent to all clients except self
        return msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
