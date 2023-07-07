from .network_router import NetworkRouter
from .....component import ComponentID


class LeafRouter(NetworkRouter):
    def __init__(self, comp_id: ComponentID):
        super().__init__(comp_id, has_client=True, has_server=False)
