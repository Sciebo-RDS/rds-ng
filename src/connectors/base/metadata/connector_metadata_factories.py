from connectors.osf.metadata import OSFMetadataFactory

from .connector_metadata_factory_catalog import ConnectorMetadataFactoryCatalog


def register_connector_metadata_factories() -> None:
    ConnectorMetadataFactoryCatalog.register_item("OSF", OSFMetadataFactory)
