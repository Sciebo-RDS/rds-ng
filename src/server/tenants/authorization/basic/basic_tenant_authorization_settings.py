import typing

from common.py.data.entities.authorization import AuthorizationSettingsConfig

from ... import Tenant


def create_basic_tenant_authorization_settings(
    tenant: Tenant,
) -> typing.Tuple[
    AuthorizationSettingsConfig | None, AuthorizationSettingsConfig | None
]:
    """
    Creates Basic tenant authorization settings.

    Args:
        tenant: The tenant.

    Returns:
        The authorization settings.
    """
    return None, None
