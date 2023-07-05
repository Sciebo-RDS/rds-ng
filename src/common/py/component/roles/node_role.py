from .component_role import ComponentRole


class NodeRole(ComponentRole):
    def __init__(self):
        from ...core.networking.routing import NodeRouter
        super().__init__(
            "Node",
            networking_aspects=ComponentRole.NetworkingAspects(has_client=True, has_server=True, router_type=NodeRouter)
        )
