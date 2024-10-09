from dataclasses import dataclass
from typing import Any, Dict, List

from common.py.data.metadata import (Metadata, MetadataCreator, MetadataParser,
                                     MetadataParserQuery)


@dataclass
class OSFMetadata(Metadata):
    title: str = None
    category: str = None
    description: str = None


class OSFMetadataCreator(MetadataCreator):
    """
    A class used to create OSF metadata objects from a list of metadata dictionaries.

    Methods
    -------
    create(metadata: List[Dict[str, Any]]) -> OSFMetadata
        Creates an OSFMetadata object from the provided metadata.
    """

    def create(self, metadata: List[Dict[str, Any]]) -> OSFMetadata:
        """
        Creates an OSFMetadata object from a list of metadata dictionaries.

        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata.

        Returns:
            OSFMetadata: An instance of OSFMetadata populated with the parsed metadata.
        """

        osf_metadata = metadata # = MetadataParser.filter_by_profile("OSF", metadata)

        product = OSFMetadata()

        product.title = MetadataParser.getattr(
            osf_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
                "title",
            ),
        )
        product.category = MetadataParser.getattr(
            osf_metadata, MetadataParserQuery("OsfCategory", "category")
        )
        product.description = MetadataParser.getattr(
            osf_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
                "abstract",
            ),
        )

        return product
