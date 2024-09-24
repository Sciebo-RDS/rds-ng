from dataclasses import dataclass
from typing import Any, Dict, List

from common.py.data.metadata import (Metadata, MetadataCreator, MetadataParser,
                                     MetadataParserQuery)
from common.py.data.metadata.datacite.utils import (parse_contributors,
                                                    parse_creators)


@dataclass
class ZenodoMetadata(Metadata):
    title: str = None
    upload_type: str = None
    description: str = None
    creators: List[Dict[str, Any]] = None
    contributors: List[Dict[str, Any]] = None


class ZenodoMetadataCreator(MetadataCreator):

    def create(metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []) -> ZenodoMetadata:

        zenodo_metadata = MetadataParser.filter_by_profile("Zenodo", metadata)

        product = ZenodoMetadata()

        product.title = MetadataParser.getattr(
            zenodo_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
                "title",
            ),
        )
        product.upload_type = MetadataParser.getattr(
            zenodo_metadata, MetadataParserQuery("ZenodoUploadType", "ZenodoUploadType")
        )
        product.description = MetadataParser.getattr(
            zenodo_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
                "abstract",
            ),
        )

        creators_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/"
            
        )

        product.creators = parse_creators(creators_raw, shared_objects)

        contributors_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/"
            
        )

        product.contributors = parse_contributors(contributors_raw, shared_objects)

        return product