import socketio

from .component_role import ComponentRole


class LeafRole(ComponentRole):
    """
    Role definition of a leaf component.
    """

    def __init__(self):
        super().__init__(
            "Leaf",
            runtime_aspects=ComponentRole.RuntimeAspects(
                runtime_app_type=socketio.WSGIApp
            ),
            networking_aspects=ComponentRole.NetworkingAspects(
                has_client=True, has_server=False
            ),
        )
