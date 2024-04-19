import dataclasses
import typing
from dataclasses import dataclass
from enum import StrEnum

from dataclasses_json import dataclass_json

ConnectorID = str
ConnectorMetadataProfile = typing.Dict[str, typing.Any]  # TODO: Use proper type


@dataclass_json
@dataclass(kw_only=True)
class Connector:
    """
    Data for a single **Connector**.

    Attributes:
        connector_id: The unique connector identifier.
        type: The connector type.
        name: The name of the connector.
        description: An optional connector description.
        logos: Image data of the connector logos.
        metadata_profile: The profile for connector-specific data.
        announce_timestamp: The timestamp when the connector was last announced.
    """

    class Type(StrEnum):
        """
        The different connector types.
        """

        UNKNOWN = ""
        REPOSITORY = "repository"
        ARCHIVE = "archive"

    @dataclass_json
    @dataclass
    class Logos:
        """
        Base64-encoded image data of the connector logos.

        Attributes:
            default_logo: The default logo.
            horizontal_logo: A logo with small height used specifically for horizontal display.
        """

        default_logo: str | None = None
        horizontal_logo: str | None = None

    connector_id: ConnectorID
    type: Type

    name: str
    description: str

    logos: Logos = dataclasses.field(default_factory=Logos)

    metadata_profile: ConnectorMetadataProfile = dataclasses.field(default_factory=dict)

    announce_timestamp: float = 0.0
