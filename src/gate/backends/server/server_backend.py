from common.py.component import BackendComponent

from ..backend import Backend


class ServerBackend(Backend):
    def __init__(self, comp: BackendComponent):
        super().__init__(
            comp,
            "Server Backend",
            [],
        )
