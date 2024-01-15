import typing

from common.py.data.entities.connector import ConnectorInstance


def fill_stub_data_connectors() -> None:
    """
    Adds some hardcoded data to the stub data storage.
    """
    from ...data.storage.memory import MemoryStoragePool

    from common.py.data.entities.connector import Connector, ConnectorID

    pool = (
        MemoryStoragePool()
    )  # The memory storage pool uses shared data objects, so we can fill them using a new instance

    from common.py.component import ComponentType

    pool.connector_storage.add(
        Connector(
            connector_id="osf",
            name="OpenScienceFramework",
            description="OSF connector",
        )
    )

    pool.connector_storage.add(
        Connector(
            connector_id="datacite",
            name="DataCite",
            description="DataCite connector",
        )
    )

    pool.connector_storage.add(
        Connector(
            connector_id="zenodo",
            name="Zenodo",
            description="Zenodo connector",
        )
    )


def fill_stub_data_connector_instances() -> None:
    from gate.backends.stub.stub_service_context import StubServiceContext

    StubServiceContext.user_configuration.connector_instances.extend(
        [
            ConnectorInstance(
                instance_id=1, connector_id="osf", name="Main OSF Account"
            ),
            ConnectorInstance(
                instance_id=2, connector_id="datacite", name="Backup DataCite"
            ),
        ]
    )
