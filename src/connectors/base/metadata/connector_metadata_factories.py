from connectors.base.metadata import ConnectorMetadataFactoryCatalog
from connectors.osf.metadata import OSFMetadataFactory


def register_connector_metadata_factories() -> None:
    ConnectorMetadataFactoryCatalog.register_item("OSF", OSFMetadataFactory)
