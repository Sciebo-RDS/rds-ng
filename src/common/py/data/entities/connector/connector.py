import dataclasses
import typing
from dataclasses import dataclass
from enum import IntFlag

from dataclasses_json import dataclass_json

from ..authorization import AuthorizationSettings
from ....utils import UnitID

ConnectorID = str
ConnectorCategoryID = str
ConnectorMetadataProfile = typing.Dict[str, typing.Any]  # TODO: Use proper type


@dataclass_json
@dataclass(kw_only=True)
class Connector:
    """
    Data for a single **Connector**.

    Attributes:
        connector_id: The unique connector identifier.
        connector_address: The target address of the connector.
        name: The name of the connector.
        description: An optional connector description.
        category: The connector category.
        authorization: Authorization settings for the connector.
        options: The connector options.
        logos: Image data of the connector logos.
        metadata_profile: The profile for connector-specific data.
        announce_timestamp: The timestamp when the connector was last announced.
    """

    class Options(IntFlag):
        """
        Options of a connector.

        Attributes:
            PUBLISH_ONCE: If set, the project may only be published once.
        """

        DEFAULT = 0x0000
        PUBLISH_ONCE = 0x0001

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
    connector_address: UnitID

    name: str
    description: str
    category: ConnectorCategoryID

    authorization: AuthorizationSettings = dataclasses.field(
        default_factory=AuthorizationSettings
    )
    options: Options = Options.DEFAULT

    logos: Logos = dataclasses.field(default_factory=Logos)

    metadata_profile: ConnectorMetadataProfile = dataclasses.field(default_factory=dict)

    announce_timestamp: float = 0.0
