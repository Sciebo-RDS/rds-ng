from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(kw_only=True, frozen=True)
class MetadataValue:
    label: str
    values: List[str] = field(default_factory=list)


@dataclass(kw_only=True, frozen=True)
class MetadataValues:
    label: str
    values: List[MetadataValue] = field(default_factory=list)


MetadataValueList = Dict[str, MetadataValues]


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
    def list_values(
        profile: Dict[str, Dict[str, Any]],
        metadata: List[Dict[str, Any]],
        shared_objects: List[Dict[str, Any]] | None = None,
    ) -> MetadataValueList:
        """
        Retrieves all (filled out) values from a profile in an easy-to-process format.
        """
        values: MetadataValueList = {}

        layout = MetadataParser.get_profile_layout(profile)
        for item in layout:
            try:
                item_id = item["id"]
                item_label = item["label"]
                item_values = MetadataParser.get_value_list(
                    metadata,
                    item_id,
                    shared_objects,
                    profile,
                )

                if len(item_values) > 0:
                    value_list: List[MetadataValue] = []
                    for v in item_values:
                        value_list.append(
                            MetadataValue(label=v["label"], values=v["values"])
                        )

                    values[item_id] = MetadataValues(
                        label=item_label, values=value_list
                    )
            except:  # pylint: disable=bare-except
                pass

        return values

    @staticmethod
    def validate_profile(profile: Dict[str, Dict[str, Any]]) -> bool:
        """
        Validates the given profile dictionary to ensure it contains the required metadata and layout information.
        Args:
            profile (Dict[str, Dict[str, Any]]): The profile dictionary to validate. It should contain 'metadata' and optionally 'layout' and 'classes'.
        Returns:
            bool: True if the profile is valid, False otherwise.
        Raises:
            ValueError: If the profile is missing required metadata keys or if the layout references missing classes.
        The profile dictionary should have the following structure:
        {
            'metadata': {
                'id': str,
                'displayLabel': str,
                'description': str,
                ...
            },
            'layout': [
                {
                    'type': str,
                    ...
                },
                ...
            ],
            'classes': {
                ...
            }
        }
        """
        try:
            if (profile_meta := profile.get("metadata")) is None:
                raise ValueError("Profile metadata is missing")

            if (
                not all(
                    e in profile_meta for e in ["id", "displayLabel", "description"]
                )
                or len(profile_meta["id"]) != 2
            ):
                raise ValueError("Profile metadata is missing required keys")

            if (layout := profile.get("layout")) is not None:
                import itertools

                types_in_layout = [e.get("type", []) for e in layout]
                types_in_layout = list(itertools.chain.from_iterable(types_in_layout))

                if not all(e in profile["classes"] for e in types_in_layout):
                    raise ValueError("Profile is missing classes referenced in layout")

            return True

        except ValueError as e:
            print(f"Validation error: {e}")
            return False

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
    def getattr(
        metadata: List[Dict[str, Any]], query: MetadataParserQuery
    ) -> List[Dict[str, Any]]:
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
    def getobj(metadata: List[Dict[str, Any]], oid: str) -> Dict[str, Any] | None:
        """
        Retrieve an object from a list of metadata dictionaries by its ID.

        Args:
            metadata (List[Dict[str, Any]]): A list of dictionaries containing metadata.
            oid (str): The ID of the object to retrieve.

        Returns:
            Dict[str, Any]: The dictionary object with the specified ID.

        Raises:
            IndexError: If no object with the specified ID is found.
        """
        if (objs := next((e for e in metadata if e["id"] == oid), None)) != None:
            print(f"Found object with ID {oid} {objs}", flush=True)
            return objs
        print(f"Object with ID {oid} not found", flush=True)
        return None

    @staticmethod
    def get_profile_layout(
        profile_metadata: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extracts the layout information from the given profile metadata.

        Args:
            profile_metadata (List[Dict[str, Any]]): A list of dictionaries containing profile metadata.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the layout information.
        """
        return profile_metadata.get("layout", [])

    @staticmethod
    def is_property_filled_out(
        metadata: List[Dict[str, Any]],
        prop_id: str,
        shared_objects: List[Dict[str, Any]] | None = None,
        profile: Dict[str, Dict[str, Any]] | None = None,
    ):
        """
        Checks if a property is filled out.

        Args:
            metadata (dict): The metadata dictionary containing various objects.
            prop_id (str): The property ID to look up in the metadata.
            shared_objects (list, optional): A list of shared objects that may be referenced in the metadata. Defaults to an empty list.
            profile (dict, optional): A dictionary containing profile information, including class layouts and templates. Defaults to an empty dictionary.
        """
        values = MetadataParser.get_value_list(
            metadata, prop_id, shared_objects, profile
        )

        if len(values) > 0:
            for value in values:
                if "values" in value and any(value["values"]):
                    return True

        return False

    @staticmethod
    def validate_metadata(
        profile: Dict[str, Dict[str, Any]],
        metadata: List[Dict[str, Any]],
        shared_objects: List[Dict[str, Any]] | None = None,
    ) -> None:
        """
        Validates all property values of a filled-out profile.

        Args:
            profile: The profile.
            metadata: The profile metadata values.
            shared_objects: List of shared objects.
        """
        layout = MetadataParser.get_profile_layout(profile)
        for item in layout:
            prop_id = item["id"]
            prop_label = item["label"]

            if not MetadataParser.is_property_valid(
                metadata, profile, prop_id, shared_objects
            ):
                error = f"The required value '{prop_label}' ({profile['metadata']['id'][0]}) is either missing or invalid"
                raise ValueError(error)

    @staticmethod
    def is_property_valid(
        metadata: List[Dict[str, Any]],
        profile: Dict[str, Dict[str, Any]],
        prop_id: str,
        shared_objects: List[Dict[str, Any]] | None = None,
    ) -> bool:
        """
        Checks if a specific property in the metadata is valid according to the given profile.
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

        if (
            property_layout := next(e for e in profile["layout"] if e["id"] == prop_id)
        ) is None:
            print(f"Property {prop_id} not defined in profile")
            return False

        if "required" not in property_layout or not property_layout["required"]:
            return True

        obj = MetadataParser.getobj(metadata, prop_id)

        if obj is None:
            print(f"Property {prop_id} is missing")
            return False

        if "input" in property_layout and len(property_layout["input"]) > 0:
            for required_value_id in [
                input["id"]
                for input in property_layout["input"]
                if "required" in input and input["required"]
            ]:
                value = MetadataParser.getattr(
                    metadata,
                    MetadataParserQuery(
                        prop_id,
                        required_value_id,
                    ),
                )
                if value is None or value == "":
                    print(
                        f"Value '{required_value_id}' is missing for property {prop_id}"
                    )
                    return False

        if not MetadataParser.is_property_filled_out(
            metadata, prop_id, shared_objects, profile
        ):
            return False

        """if "type" in property_layout and len(property_layout["type"]) > 0:
            if "required" in property_layout and property_layout["required"]:
                if "refs" not in obj or len(obj["refs"]) == 0:
                    print(
                        f"{property_layout['label']} does not have any refs, but is has types {property_layout['type']}"
                    )
                    return False"""

        return True

    @staticmethod
    def _transform_simple_values(obj, profile):
        values = []

        if (
            obj_profile := next(e for e in profile["layout"] if e["id"] == obj["id"])
        ) is None or "value" not in obj:
            return values

        for key, value in obj["value"].items():

            value_definition = next(
                (e for e in obj_profile["input"] if e["id"] == key), None
            )

            if not value_definition or "label" not in value_definition:
                continue

            label = value_definition["label"]
            value = {
                "label": label,
                "values": [value] if isinstance(value, list) else [value],
            }

            values.append(value)

        return values

    @staticmethod
    def _transform_complex_values(obj, shared_objects, profile):
        values = []
        objs = [
            MetadataParser.getobj(shared_objects, ref) for ref in obj.get("refs", [])
        ]

        def _replace_template(obj, template, profile):
            import re

            result = template
            matches = re.findall("\${[a-zA-z0-9]*}", result)

            for match in [m for m in matches if m is not None]:
                fallback_str = f"{{{next(e for e in profile['classes'][obj['type']]['input'] if e['id'] == match[2:-1])['label']}}}"
                replacement_str = obj["value"].get(match[2:-1], fallback_str)
                result = result.replace(result, replacement_str)

            return result

        for obj in [o for o in objs if o]:
            type = obj["type"]
            property_layout = profile["classes"][type]

            replaced_template = _replace_template(
                obj, property_layout["labelTemplate"], profile
            )

            if property_layout["label"] not in [e["label"] for e in values if e]:
                values.append(
                    {"label": property_layout["label"], "values": [replaced_template]}
                )

                continue

            for v in values:
                if v["label"] == property_layout["label"]:
                    v["values"].append(replaced_template)
                    break

        return values

    @staticmethod
    def get_value_list(
        metadata: List[Dict[str, Any]],
        prop_id: str,
        shared_objects: List[Dict[str, Any]] | None = None,
        profile: Dict[str, Dict[str, Any]] | None = None,
    ) -> List[Dict[str, str]]:
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

        if shared_objects is None:
            shared_objects = []

        if profile is None:
            profile = {}

        try:
            if (
                obj := MetadataParser.getobj(metadata, prop_id)
            ) == [] or not MetadataParser.validate_profile(profile):
                return []

        except Exception as e:
            print(f"Exception: {e}")
            return []

        return MetadataParser._transform_simple_values(
            obj, profile
        ) + MetadataParser._transform_complex_values(obj, shared_objects, profile)
