import typing
from dataclasses import asdict

from common.py.data.entities.properties.properties_profile import PropertyProfile

from .. import clone_entity
from .connector import Connector, ConnectorID


def find_connector_by_id(
    connectors: typing.List[Connector], connector_id: ConnectorID
) -> Connector | None:
    """
    Searches for a connector by its ID within a list of connectors.

    Args:
        connectors: The list of connectors.
        connector_id: The connector to search for.

    Returns:
        The found connector or **None** otherwise.
    """
    matching_connector = (con for con in connectors if con.connector_id == connector_id)
    return next(matching_connector, None)


def apply_connector_update(
    connector: Connector,
    updated_connector: Connector,
) -> None:
    """
    Applies an update to a connector.

    Args:
        connector: The connector to apply the update to.
        updated_connector: The updated connector.
    """

    connector.name = updated_connector.name
    connector.description = updated_connector.description
    connector.category = updated_connector.category
    connector.authorization = updated_connector.authorization
    connector.options = updated_connector.options
    connector.logos = clone_entity(updated_connector.logos)
    connector.metadata_profile = PropertyProfile(
        **asdict(updated_connector.metadata_profile)
    )
    connector.announce_timestamp = updated_connector.announce_timestamp
