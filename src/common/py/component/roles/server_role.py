from .component_role import ComponentRole


class ServerRole(ComponentRole):
    """
    Role definition of a server component.
    """
    def __init__(self):
        super().__init__(
            "Server",
            networking_aspects=ComponentRole.NetworkingAspects(has_client=False, has_server=True)
        )
