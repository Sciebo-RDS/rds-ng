from .component_role import ComponentRole


class ServerRole(ComponentRole):
    def __init__(self):
        from .aspects import NetworkingAspects
        
        super().__init__(
            "Leaf",
            networking_aspects=NetworkingAspects(has_client=False, has_server=True)
        )

