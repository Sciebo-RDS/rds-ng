import typing

from common.py.data.entities.authorization import AuthorizationSettings
from common.py.integration.authorization.strategies.oauth2 import (
    OAuth2StrategyPrivateConfiguration,
)

from .tenant import Tenant


def authorization_settings_from_tenant(
    strategy: str, tenant: Tenant
) -> AuthorizationSettings:
    """
    Creates authorization settings for the given strategy from a tenant.

    Args:
        strategy: The strategy to use.
        tenant: The tenant.

    Returns:
        The authorization settings.
    """
    from common.py.integration.authorization.strategies.oauth2 import OAuth2Strategy

    config: typing.Dict[str, typing.Any] = {}

    if strategy == OAuth2Strategy.Strategy:
        config = OAuth2StrategyPrivateConfiguration(
            client=OAuth2StrategyPrivateConfiguration.Client(
                client_secret=tenant.private_config.authorization.oauth2.client_secret
            )
        ).to_dict()

    return AuthorizationSettings(strategy=strategy, config=config)
