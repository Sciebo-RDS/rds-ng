import typing

from common.py.data.entities.authorization import AuthorizationSettings
from common.py.integration.authorization.strategies.basic import BasicStrategy
from common.py.integration.authorization.strategies.bearer import BearerStrategy
from common.py.integration.authorization.strategies.oauth2 import OAuth2Strategy

from .tenant_authorization_settings_catalog import (
    TenantAuthorizationSettingsCatalog,
)
from .. import Tenant


def register_tenant_authorization_settings_creators() -> None:
    """
    Registers all available strategy-specific tenant authorization settings creators.

    When adding a new strategy, always register it here.
    """

    from .basic import create_basic_tenant_authorization_settings
    from .bearer import create_bearer_tenant_authorization_settings
    from .oauth2 import create_oauth2_tenant_authorization_settings

    # New strategies go here
    TenantAuthorizationSettingsCatalog.register_item(
        OAuth2Strategy.Strategy, create_oauth2_tenant_authorization_settings
    )
    TenantAuthorizationSettingsCatalog.register_item(
        BasicStrategy.Strategy, create_basic_tenant_authorization_settings
    )
    TenantAuthorizationSettingsCatalog.register_item(
        BearerStrategy.Strategy, create_bearer_tenant_authorization_settings
    )


def create_tenant_authorization_settings(
    strategy: str,
    tenant: Tenant,
) -> typing.Tuple[AuthorizationSettings | None, AuthorizationSettings | None]:
    """
    Creates new strategy-specific tenant authorization settings.

    Args:
        tenant: The tenant.
        strategy: The strategy identifier.

    Returns:
        The newly created authorization settings (public and private).
    """
    if strategy == "":
        raise RuntimeError("No authorization strategy has been provided")

    settings_creator = TenantAuthorizationSettingsCatalog.find_item(strategy)
    if settings_creator is None:
        raise RuntimeError(f"No settings creator registered for strategy '{strategy}'")

    public_settings, private_settings = settings_creator(tenant)
    auth_public = (
        AuthorizationSettings(strategy=strategy, config=public_settings)
        if public_settings is not None
        else None
    )
    auth_private = (
        AuthorizationSettings(strategy=strategy, config=private_settings)
        if private_settings is not None
        else None
    )

    return auth_public, auth_private
