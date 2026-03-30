import typing

from common.py.data.entities.authorization import AuthorizationSettingsConfig
from common.py.integration.authorization.strategies.oauth2 import (
    OAuth2StrategyPrivateConfiguration,
)

from ... import Tenant


def create_oauth2_tenant_authorization_settings(
    tenant: Tenant,
) -> typing.Tuple[
    AuthorizationSettingsConfig | None, AuthorizationSettingsConfig | None
]:
    """
    Creates OAuth2 tenant authorization settings.

    Args:
        tenant: The tenant.

    Returns:
        The authorization settings.
    """
    private_config = OAuth2StrategyPrivateConfiguration(
        client=OAuth2StrategyPrivateConfiguration.Client(
            client_secret=tenant.private_config.authorization.oauth2.client_secret
        )
    )

    return None, private_config.to_dict()
