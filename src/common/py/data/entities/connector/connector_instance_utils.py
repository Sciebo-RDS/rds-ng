import typing

from .connector import Connector
from .connector_instance import ConnectorInstanceID, ConnectorInstance


def find_connector_instance_by_id(
    connector_instances: typing.List[ConnectorInstance],
    instance_id: ConnectorInstanceID,
) -> ConnectorInstance | None:
    """
    Searches for a connector instance by its ID within a list of connector instances.

    Args:
        connector_instances: The list of connector instances.
        instance_id: The connector instance to search for.

    Returns:
        The found connector instance or **None** otherwise.
    """
    matching_instance = (
        inst for inst in connector_instances if inst.instance_id == instance_id
    )
    return next(matching_instance, None)


def find_connector_by_instance_id(
    connectors: typing.List[Connector],
    connector_instances: typing.List[ConnectorInstance],
    instance_id: ConnectorInstanceID,
) -> Connector | None:
    """
    Retrieves the connector that is indirectly specified by a connector instance.

    Args:
        connectors: The list of connectors.
        connector_instances: The list of connector instances.
        instance_id: The connector instance to search for.

    Returns:
        The found connector or **None** otherwise.
    """
    if (
        connector_instance := find_connector_instance_by_id(
            connector_instances, instance_id
        )
    ) is not None:
        from .connector_utils import find_connector_by_id

        return find_connector_by_id(connectors, connector_instance.connector_id)

    return None
