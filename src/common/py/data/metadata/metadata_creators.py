from common.py.data.metadata.datacite.datacite import DataciteMetadataCreator

from .metadata_creator_catalog import MetadataCreatorCatalog


def register_metadata_creators() -> None:
    MetadataCreatorCatalog.register_item("DataCite", DataciteMetadataCreator)