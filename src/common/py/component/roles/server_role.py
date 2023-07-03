from .component_role import ComponentRole


class ServerRole(ComponentRole):
    def __init__(self):
        from .aspects import MessagingAspects, NetworkingAspects
        from ...core.messaging.routing import ServerRouter as ServerMessageRouter
        
        super().__init__(
            "Leaf",
            messaging_aspects=MessagingAspects(message_router_type=ServerMessageRouter),
            networking_aspects=NetworkingAspects(has_client=True, has_server=True)
        )

