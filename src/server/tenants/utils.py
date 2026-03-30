from common.py.data.entities.connector import ConnectorID

from .tenant import Tenant


def exclude_connector_for_tenant(tenant: Tenant, connector: ConnectorID) -> bool:
    """
    Checks whether to exclude a connector for a given tenant.

    Args:
        tenant: The tenant.
        connector: The connector to check.
    """
    return connector in tenant.private_config.connectors.excluded_connectors
