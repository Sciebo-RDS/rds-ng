from common.py.component import BackendComponent

from ..backend import Backend


class StubBackend(Backend):
    def __init__(self, comp: BackendComponent):
        # Add some initial data to the in-memory storage
        from .stub_data_connectors import (
            fill_stub_data_connectors,
            fill_stub_data_connector_instances,
        )
        from .stub_data_projects import fill_stub_data_projects

        fill_stub_data_connectors()
        fill_stub_data_connector_instances()
        fill_stub_data_projects()

        # Create all stub services
        from .stub_connectors_service import create_stub_connectors_service
        from .stub_projects_service import create_stub_projects_service
        from .stub_users_service import create_stub_users_service

        super().__init__(
            comp,
            "Stub Backend",
            [
                create_stub_connectors_service(comp),
                create_stub_users_service(comp),
                create_stub_projects_service(comp),
            ],
        )
