from common.py.component import BackendComponent

from ..backend import Backend


class StubBackend(Backend):
    def __init__(self, comp: BackendComponent):
        from .stub_projects_service import create_stub_projects_service

        super().__init__(
            comp,
            "Stub Backend",
            [
                create_stub_projects_service(comp),
            ],
        )
