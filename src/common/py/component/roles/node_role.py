from .component_role import ComponentRole


class NodeRole(ComponentRole):
    def __init__(self):
        super().__init__(
            "Node",
            networking_aspect=ComponentRole.NetworkingAspect(has_client=True, has_server=True)
        )
