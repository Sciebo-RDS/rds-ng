from .component_role import ComponentRole


class NodeRole(ComponentRole):
    def __init__(self):
        from .aspects import NetworkingAspects
        
        super().__init__(
            "Node",
            networking_aspects=NetworkingAspects(has_client=True, has_server=True)
        )
