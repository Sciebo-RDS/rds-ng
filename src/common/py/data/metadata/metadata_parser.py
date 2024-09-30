from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class MetadataParserQuery:
    """
    MetadataParserQuery is a data class that represents a query for metadata parsing.

    Attributes:
        id (str): The identifier for the metadata query.
        value (str): The value associated with the metadata query.
    """
    id: str
    value: str


class MetadataParser:
    """
    MetadataParser class provides static methods to filter and retrieve metadata based on profiles and queries.
    Methods:
        filter_by_profile(profile_name: str | List, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            Filters the metadata entries by the given profile name(s).
        getattr(metadata: List[Dict[str, Any]], query: MetadataParserQuery) -> List[Dict[str, Any]]:
            Retrieves the value from metadata entries based on the given query.
        getobj(metadata: List[Dict[str, Any]], id: str):
            Retrieves the metadata entry with the specified id.
    """

    @staticmethod
    def filter_by_profile(
        profile_name: str | List, metadata: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        
        """
        Filters the metadata by the given profile name(s).

        Args:
            profile_name (str | List): A single profile name or a list of profile names to filter by.
            metadata (List[Dict[str, Any]]): A list of metadata dictionaries, each containing a "profiles" key.

        Returns:
            List[Dict[str, Any]]: A list of metadata dictionaries that match the given profile name(s).
        """
        
        if isinstance(profile_name, str):
            profile_name = [profile_name]

        return list(
            filter(
                lambda y: any(
                    profile in map(lambda z: z[0], y["profiles"])
                    for profile in profile_name
                ),
                metadata,
            )
        )

    @staticmethod
    def getattr(metadata: List[Dict[str, Any]], query: MetadataParserQuery) -> List[Dict[str, Any]]:
        """
        Retrieve a list of dictionaries from metadata based on a query.

        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata.
            query (MetadataParserQuery): An object containing the query parameters with 'id' and 'value' attributes.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries that match the query criteria, or None if no match is found.
        """
        return next(
            (
                e["value"][query.value]
                for e in metadata
                if e["id"] == query.id and query.value in e["value"]
            ),
            None,
        )
    
    @staticmethod
    def getobj(metadata: List[Dict[str, Any]], id: str):
        """
        Retrieve an object from a list of metadata dictionaries by its ID.

        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata.
            id (str): The ID of the object to retrieve.

        Returns:
            Dict[str, Any]: The dictionary object with the specified ID.

        Raises:
            IndexError: If no object with the specified ID is found.
        """
        return [e for e in metadata if e['id'] == id][0]
