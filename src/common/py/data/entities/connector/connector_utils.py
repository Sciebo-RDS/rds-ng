import typing

from .connector import ConnectorID, Connector
from .. import clone_entity


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
    connector.logos = clone_entity(updated_connector.logos)
    connector.metadata_profile = updated_connector.metadata_profile.copy()
    connector.announce_timestamp = updated_connector.announce_timestamp
