from dataclasses import dataclass, field
from typing import Any, Dict, List

from common.py.data.entities.properties import PropertyObject
from common.py.data.metadata import (
    Metadata,
    MetadataCreator,
    MetadataParser,
    MetadataParserQuery,
)

from .utils import parse_contributors, parse_creators, parse_dates, parse_grants


@dataclass
class InvenioRDMMetadata(Metadata):
    title: str = ""
    upload_type: str = ""
    description: str = ""
    version: str = ""
    creators: List[Dict[str, Any]] = field(default_factory=list)
    contributors: List[Dict[str, Any]] = field(default_factory=list)
    subjects: List[Dict[str, Any]] = field(default_factory=list)
    grants: List[Dict[str, Any]] = field(default_factory=list)
    dates: List[Dict[str, Any]] = field(default_factory=list)


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
        product.upload_type = MetadataParser.getattr(
            inveniordm_metadata,
            MetadataParserQuery("InvenioRDMUploadType", "InvenioRDMUploadType"),
        )
        product.description = MetadataParser.getattr(
            inveniordm_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
                "abstract",
            ),
        )

        product.version = MetadataParser.getattr(
            inveniordm_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/version/",
                "version",
            ),
        )

        creators_raw = MetadataParser.getobj(
            inveniordm_metadata,
            "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/",
        )

        product.creators = (
            parse_creators(creators_raw, shared_objects) if creators_raw else []
        )

        contributors_raw = MetadataParser.getobj(
            inveniordm_metadata,
            "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/",
        )

        product.contributors = (
            parse_contributors(contributors_raw, shared_objects)
            if contributors_raw
            else []
        )

        # subjects_raw = MetadataParser.getobj(
        #    InvenioRDM_metadata,
        #        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/subject/"

        # )

        # product.subjects = parse_subjects(subjects_raw, shared_objects) if subjects_raw else []

        grants_raw = MetadataParser.getobj(
            inveniordm_metadata,
            "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/fundingreference/",
        )

        product.grants = parse_grants(grants_raw, shared_objects) if grants_raw else []

        dates_raw = MetadataParser.getobj(
            inveniordm_metadata,
            "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/date/",
        )

        product.dates = parse_dates(dates_raw, shared_objects) if dates_raw else []

        return product
