from common.py.component import BackendComponent

from ..backend import Backend


class StubBackend(Backend):
    def __init__(self, comp: BackendComponent):
        # Add some initial data to the in-memory storage
        from .data import get_stub_data_connectors, get_stub_data_projects
        from ...data.storage.memory import MemoryConnectorStorage, MemoryProjectStorage

        # Add default data to all storages
        MemoryConnectorStorage.default_connectors = get_stub_data_connectors()
        MemoryProjectStorage.default_projects = get_stub_data_projects()

        # Create all stub services
        from .services import (
            create_stub_connectors_service,
            create_stub_projects_service,
            create_stub_users_service,
            create_stub_resources_service,
        )

        super().__init__(
            comp,
            "Stub Backend",
            [
                create_stub_connectors_service(comp),
                create_stub_users_service(comp),
                create_stub_projects_service(comp),
                create_stub_resources_service(comp),
            ],
        )
