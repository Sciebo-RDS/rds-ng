from .component_role import ComponentRole


class NodeRole(ComponentRole):
    def __init__(self):
        from .aspects import MessagingAspects, NetworkingAspects
        from ...core.messaging.routing import NodeRouter as NodeMessageRouter
        
        super().__init__(
            "Node",
            messaging_aspects=MessagingAspects(message_router_type=NodeMessageRouter),
            networking_aspects=NetworkingAspects(has_client=True, has_server=True)
        )

