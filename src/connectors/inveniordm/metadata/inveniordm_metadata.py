from dataclasses import dataclass
from typing import Dict, List

from common.py.data.entities.properties import PropertyObject
from common.py.data.metadata import (
    Metadata,
    MetadataCreator,
    MetadataParser,
    MetadataParserQuery,
)


@dataclass
class InvenioRDMMetadata(Metadata):
    title: str = ""


class InvenioRDMMetadataCreator(MetadataCreator):
    """
    A class to create InvenioRDM metadata from a given list of metadata and shared objects.
    Methods
    -------
    create(metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []) -> InvenioRDMMetadata:
        Creates a InvenioRDMMetadata object from the provided metadata and shared objects.
    """

    def create(
        self, metadata: List[PropertyObject], shared_objects: List[PropertyObject] = []
    ) -> InvenioRDMMetadata:
        """
        Create a InvenioRDMMetadata object from provided metadata and shared objects.
        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata information.
            shared_objects (List[Dict[str, Any]], optional): A list of dictionaries containing shared objects. Defaults to an empty list.
        Returns:
            InvenioRDMMetadata: An instance of InvenioRDMMetadata populated with the parsed metadata.
        """

        inveniordm_metadata = (
            metadata  # = MetadataParser.filter_by_profile("InvenioRDM", metadata)
        )

        product = InvenioRDMMetadata()

        product.title = MetadataParser.getattr(
            inveniordm_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
                "title",
            ),
        )

        return product
