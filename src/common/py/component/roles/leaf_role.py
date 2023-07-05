from .component_role import ComponentRole


class LeafRole(ComponentRole):
    def __init__(self):
        super().__init__(
            "Leaf",
            networking_aspect=ComponentRole.NetworkingAspect(has_client=True, has_server=False)
        )
