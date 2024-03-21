from common.py.component import BackendComponent

from ..backend import Backend


class ServerBackend(Backend):
    def __init__(self, comp: BackendComponent):
        # Create all stub services
        from .services import create_server_backend_service

        super().__init__(
            comp,
            "Server Backend",
            [create_server_backend_service(comp)],
        )
