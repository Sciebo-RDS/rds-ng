from .component_role import ComponentRole


class LeafRole(ComponentRole):
    def __init__(self):
        from .aspects.networking_aspects import NetworkingAspects
        
        super().__init__(
            "Leaf",
            networking_aspects=NetworkingAspects(has_client=True, has_server=False)
        )
