from .component_role import ComponentRole


class ServerRole(ComponentRole):
    def __init__(self):
        from ...core.messaging.networking.routing import ServerRouter
        super().__init__(
            "Leaf",
            networking_aspects=ComponentRole.NetworkingAspects(has_client=False, has_server=True, router_type=ServerRouter)
        )

