from typing import Any, Dict, List

from common.py.data.metadata import (
    MetadataParser,
)
from common.py.data.metadata.metadata import MetadataCreator
from .utils import parse_metadata

Metadata = DataciteMetadata = List[Dict[str, Any]]


class DataciteMetadataCreator(MetadataCreator):

    def create(
        self, metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []
    ) -> DataciteMetadata:
        """
        Creates a DataciteMetadata object from the provided metadata and shared objects.

        Args:
                metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata information.
                shared_objects (List[Dict[str, Any]], optional): A list of dictionaries containing shared objects. Defaults to an empty list.

        Returns:
                DataciteMetadata: The parsed Datacite metadata object.
        """
        datacite_metadata = MetadataParser.filter_by_profile("DataCite", metadata)

        return parse_metadata(datacite_metadata, shared_objects)
