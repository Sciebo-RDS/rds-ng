from .component_role import ComponentRole


class LeafRole(ComponentRole):
    def __init__(self):
        from ...core.messaging.networking.routing import LeafRouter
        super().__init__(
            "Leaf",
            networking_aspects=ComponentRole.NetworkingAspects(has_client=True, has_server=False, router_type=LeafRouter)
        )
