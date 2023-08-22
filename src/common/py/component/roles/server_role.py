import socketio

from .component_role import ComponentRole


class ServerRole(ComponentRole):
    """
    Role definition of a server component.
    """

    def __init__(self):
        super().__init__(
            "Server",
            runtime_aspects=ComponentRole.RuntimeAspects(
                runtime_app_type=socketio.WSGIApp
            ),
            networking_aspects=ComponentRole.NetworkingAspects(
                has_client=False, has_server=True
            ),
        )
