from common.py.data.metadata.datacite.datacite import DataciteMetadataCreator
from connectors.osf.metadata import OSFMetadataCreator
from connectors.zenodo.metadata import ZenodoMetadataCreator

from .metadata_creator_catalog import MetadataCreatorCatalog


def register_metadata_creators() -> None:
    MetadataCreatorCatalog.register_item("DataCite", DataciteMetadataCreator)
    MetadataCreatorCatalog.register_item("OSF", OSFMetadataCreator)
    MetadataCreatorCatalog.register_item("Zenodo", ZenodoMetadataCreator)
