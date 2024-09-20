from connectors.osf.metadata import OSFMetadataCreator

from .metadata_creator_catalog import MetadataCreatorCatalog


def register_metadata_creators() -> None:
    MetadataCreatorCatalog.register_item("OSF", OSFMetadataCreator)
