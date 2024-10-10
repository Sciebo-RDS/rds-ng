import json
from dataclasses import dataclass
from typing import Any, Dict, List

from metadata.utils import (parse_contributors, parse_creators, parse_dates,
                            parse_grants, parse_subjects)

from common.py.data.metadata import (Metadata, MetadataCreator, MetadataParser,
                                     MetadataParserQuery)


@dataclass
class ZenodoMetadata(Metadata):
    title: str = None
    upload_type: str = None
    description: str = None
    version: str = None
    creators: List[Dict[str, Any]] = None
    contributors: List[Dict[str, Any]] = None
    subjects: List[Dict[str, Any]] = None
    grants: List[Dict[str, Any]] = None
    dates: List[Dict[str, Any]] = None


class ZenodoMetadataCreator(MetadataCreator):
    """
    A class to create Zenodo metadata from a given list of metadata and shared objects.
    Methods
    -------
    create(metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []) -> ZenodoMetadata:
        Creates a ZenodoMetadata object from the provided metadata and shared objects.
    """

    def create(self, metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []) -> ZenodoMetadata:
        """
        Create a ZenodoMetadata object from provided metadata and shared objects.
        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata information.
            shared_objects (List[Dict[str, Any]], optional): A list of dictionaries containing shared objects. Defaults to an empty list.
        Returns:
            ZenodoMetadata: An instance of ZenodoMetadata populated with the parsed metadata.
        """

        zenodo_metadata = metadata # = MetadataParser.filter_by_profile("Zenodo", metadata)

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

        product.version = MetadataParser.getattr(
            zenodo_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/version/",
                "version",
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

        subjects_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/subject/"
            
        )

        product.subjects = parse_subjects(subjects_raw, shared_objects)

        grants_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/fundingreference/"
            
        )
        
        product.grants = parse_grants(grants_raw, shared_objects)


        

        dates_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/date/"
            
        )
        
        product.dates = parse_dates(dates_raw, shared_objects)

        return product