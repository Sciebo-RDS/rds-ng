from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Dict, List

from common.py.data.metadata import (Metadata, MetadataCreator, MetadataParser,
                                     MetadataParserQuery)


@dataclass
class OSFMetadata(Metadata):
    title: str = None
    category: str = None
    description: str = None


class OSFMetadataCreator(MetadataCreator):

    def create(metadata: List[Dict[str, Any]]) -> OSFMetadata:

        osf_metadata = MetadataParser.filter_by_profile("OSF", metadata)

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
