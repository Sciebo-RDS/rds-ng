from dataclasses import dataclass
from typing import Any, Dict, List


class MetadataPropertyMissingError(Exception):
    pass

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
    def getobj(metadata: List[Dict[str, Any]], id: str) -> Dict[str, Any]:
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
        if len(objs := [e for e in metadata if e['id'] == id]) > 0:
            return objs[0]
        return


    @staticmethod
    def get_profile_layout(profile_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extracts the layout information from the given profile metadata.

        Args:
            profile_metadata (List[Dict[str, Any]]): A list of dictionaries containing profile metadata.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the layout information.
        """
        return profile_metadata['layout']

    @staticmethod
    def is_property_filled_out(metadata, profile, prop_id):
        """
        Checks if a specific property in the metadata is filled out according to the given profile.
        Args:
            metadata (dict): The metadata dictionary containing various properties.
            profile (dict): The profile dictionary that defines the layout and requirements for properties.
            prop_id (str): The identifier of the property to check.
        Returns:
            bool: True if the property is filled out according to the profile, False otherwise.
        Raises:
            MetadataPropertyMissingError: If the property is missing in the metadata or not defined in the profile.
        Notes:
            - The function first checks if the property exists in the metadata.
            - It then verifies if the property is defined in the profile layout.
            - If the property has required input values, it checks if those values are present and non-empty.
            - If the property has a type defined in the profile, it ensures that the property has references.
        """

        obj = MetadataParser.getobj(metadata, prop_id)
        
        if obj == None:
            raise MetadataPropertyMissingError(f"Property {prop_id} is missing")
        
        if len(property_layout := [e for e in profile['layout'] if e['id'] == prop_id]) == 0:
            raise MetadataPropertyMissingError(f"Property {prop_id} not defined in profile")
        
        property_layout = property_layout[0]

        if "input" in property_layout and len(property_layout['input']) > 0:

            for required_value_id in [input['id'] for input in property_layout['input'] if 'required' in input and input['required']]:
                value = MetadataParser.getattr(
                    metadata,
                    MetadataParserQuery(
                        prop_id,
                        required_value_id,
                    ),
                )
                if value == None or value == '':
                    print(f"Value {required_value_id} is missing for property {prop_id}")
                    return False
                
        if "type" in property_layout and len(property_layout['type']) > 0:
            if "refs" not in obj or len(obj['refs']) == 0:
                print(f"{property_layout['label']} does not have any refs, but is has types {property_layout['type']}")
                return False

        return True

    @staticmethod
    def get_value_list(metadata, prop_id, shared_objects = [], profile = {}):
        """
        Retrieves a dictionary of values based on the provided metadata, property ID, shared objects, and profile.

        Args:
            metadata (dict): The metadata dictionary containing various objects.
            prop_id (str): The property ID to look up in the metadata.
            shared_objects (list, optional): A list of shared objects that may be referenced in the metadata. Defaults to an empty list.
            profile (dict, optional): A dictionary containing profile information, including class layouts and templates. Defaults to an empty dictionary.

        Returns:
            dict: A dictionary of values where keys are object IDs and values are the transformed values based on the metadata and profile.
        """
        
        values = {}

        def _transform_simple_values(obj):
            return obj['value'] if 'value' in obj else {}

        def _transform_complex_values(obj, shared_objects, profile, prop_id):
            values = {}
            objs = [MetadataParser.getobj(shared_objects, ref) for ref in obj['refs']]

            def _replace_template(obj, template, profile):
                import re
                result = template
                matches = re.findall("\${[a-zA-z0-9]*}", result)

                for match in [m for m in matches if m != None]:
                    result = result.replace(result, obj['value'].get(match[2:-1], f"[{[e for e in profile['classes'][obj['type']]['input'] if e['id'] == match[2:-1]][0]['label']}]"))

                return result

            for obj in [o for o in objs if o != None]:
                type = obj['type']
                property_layout = profile['classes'][type]

                values[obj['id']] = _replace_template(obj, property_layout['labelTemplate'], profile)

            return values

        if (obj := MetadataParser.getobj(metadata, prop_id)) != []:
            values = values | _transform_simple_values(obj) | _transform_complex_values(obj, shared_objects, profile, prop_id)

        return values