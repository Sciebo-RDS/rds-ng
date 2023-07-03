from .component_role import ComponentRole


class LeafRole(ComponentRole):
    def __init__(self):
        from .aspects import MessagingAspects, NetworkingAspects
        from ...core.messaging.routing import LeafRouter as LeafMessageRouter
        
        super().__init__(
            "Leaf",
            messaging_aspects=MessagingAspects(message_router_type=LeafMessageRouter),
            networking_aspects=NetworkingAspects(has_client=True, has_server=False)
        )
