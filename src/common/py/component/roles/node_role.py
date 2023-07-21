import socketio

from .component_role import ComponentRole


class NodeRole(ComponentRole):
    """
    Role definition of a node component.
    """
    def __init__(self):
        super().__init__(
            "Node",
            runtime_aspects=ComponentRole.RuntimeAspects(runtime_app_type=socketio.WSGIApp),
            networking_aspects=ComponentRole.NetworkingAspects(has_client=True, has_server=True)
        )
