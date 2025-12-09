import typing
from dataclasses import dataclass
from typing import List

from common.py.data.entities.properties import PropertyObject
from common.py.data.metadata import (
    Metadata,
    MetadataCreator,
    MetadataParser,
    MetadataParserQuery,
)
from connectors.dataverse.metadata.utils import parse_authors, parse_pocs

from .utils import (
    DataverseAuthor,
    DataversePointOfContact,
    DataverseRights,
    parse_rights,
)


@dataclass
class DataverseMetadata(Metadata):
    title: str
    authors: List[DataverseAuthor]
    pocs: List[DataversePointOfContact]
    description: str
    subject: List[str]
    rights: DataverseRights


class DataverseMetadataBuilder:
    def __init__(self):
        self._title: str | None = None
        self._authors: List[DataverseAuthor] | None = None
        self._pocs: List[DataversePointOfContact] | None = None
        self._description: str | None = None
        self._subject: List[str] | None = None
        self._rights: DataverseRights | None = None

    def with_title(self, metadata: List[PropertyObject]) -> typing.Self:
        self._title = MetadataParser.getattr(
            metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
                "title",
            ),
        )
        return self

    def with_authors(
        self,
        metadata: List[PropertyObject],
        shared_objects: List[PropertyObject] | None = None,
    ) -> typing.Self:
        if shared_objects is None:
            shared_objects = []

        authors_raw = MetadataParser.getobj(metadata, "dataverseAuthor")

        self._authors = (
            parse_authors(authors_raw, shared_objects) if authors_raw else []
        )

        return self

    def with_pocs(
        self,
        metadata: List[PropertyObject],
        shared_objects: List[PropertyObject] | None = None,
    ) -> typing.Self:
        if shared_objects is None:
            shared_objects = []

        pocs_raw = MetadataParser.getobj(metadata, "dataversePOC")

        self._pocs = parse_pocs(pocs_raw, shared_objects) if pocs_raw else []

        return self

    def with_description(self, metadata: List[PropertyObject]) -> typing.Self:
        self._description = MetadataParser.getattr(
            metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
                "abstract",
            ),
        )

        return self

    def with_subject(self, metadata: List[PropertyObject]) -> typing.Self:
        self._subject = MetadataParser.getattr(
            metadata,
            MetadataParserQuery(
                "dataverseSubject",
                "dSubject",
            ),
        )

        return self

    def with_rights(
        self, metadata: List[PropertyObject], shared_objects: List[PropertyObject] = []
    ) -> typing.Self:
        rights_raw = MetadataParser.getobj(metadata, "rights")

        self._rights = parse_rights(rights_raw, shared_objects)

        return self

    def build(self) -> DataverseMetadata:
        if not self._title:
            raise ValueError("Title is required")
        if not self._authors:
            raise ValueError("Author is required")
        if not self._pocs:
            raise ValueError("Points of contact is required")
        if not self._description:
            raise ValueError("Description is required")
        if not self._subject:
            raise ValueError("Subject is required")
        if not self._rights:
            raise ValueError("Rights are required")

        return DataverseMetadata(
            title=self._title,
            authors=self._authors,
            pocs=self._pocs,
            description=self._description,
            subject=self._subject,
            rights=self._rights,
        )


class DataverseMetadataCreator(MetadataCreator):
    """
    A class used to create Dataverse metadata objects from a list of metadata dictionaries.

    Methods
    -------
    create(metadata: List[Dict[str, Any]], shared_objects: List[PropertyObject] = []) -> DataverseMetadata
        Creates a DataverseMetadata object from the provided metadata.
    """

    def create(
        self,
        metadata: List[PropertyObject],
        shared_objects: List[PropertyObject] | None = None,
    ) -> DataverseMetadata:
        """
        Creates an DataverseMetadata object from a list of metadata dictionaries.

        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata.
            shared_objects (List[PropertyObject]): A list of shared PropertyObjects.

        Returns:
            DataverseMetadata: An instance of DataverseMetadata populated with the parsed metadata.
        """

        return (
            DataverseMetadataBuilder()
            .with_title(metadata)
            .with_authors(metadata, shared_objects)
            .with_pocs(metadata, shared_objects)
            .with_description(metadata)
            .with_subject(metadata)
            .with_rights(metadata)
            .build()
        )
