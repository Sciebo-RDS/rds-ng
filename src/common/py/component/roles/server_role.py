from .component_role import ComponentRole


class ServerRole(ComponentRole):
    def __init__(self):
        from .aspects.networking_aspects import NetworkingAspects
        
        super().__init__(
            "Server",
            networking_aspects=NetworkingAspects(has_client=True, has_server=True)
        )
