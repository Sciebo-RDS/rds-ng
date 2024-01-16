import typing

from .connector import ConnectorID, Connector


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
