def fill_stub_data_connectors() -> None:
    """
    Adds some hardcoded data to the stub data storage.
    """
    from ...data.storage.memory import MemoryStoragePool

    from common.py.data.entities import Connector, ConnectorID

    pool = (
        MemoryStoragePool()
    )  # The memory storage pool uses shared data objects, so we can fill them using a new instance

    from common.py.component import ComponentType

    pool.connector_storage.add(
        Connector(
            connector_id=ConnectorID(ComponentType.CONNECTOR, "osf"),
            name="OpenScienceFramework",
            description="OSF connector",
        )
    )

    pool.connector_storage.add(
        Connector(
            connector_id=ConnectorID(ComponentType.CONNECTOR, "datacite"),
            name="DataCite",
            description="DataCite connector",
        )
    )

    pool.connector_storage.add(
        Connector(
            connector_id=ConnectorID(ComponentType.CONNECTOR, "zenodo"),
            name="Zenodo",
            description="Zenodo connector",
        )
    )
