import typing

from .authorization_strategies_catalog import AuthorizationStrategiesCatalog
from .authorization_strategy import AuthorizationStrategy
from .oauth2 import (
    OAuth2Strategy,
    create_oauth2_strategy,
)
from ....component import BackendComponent
from ....core import logging
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.user import UserToken
from ....services import Service


def register_authorization_strategies() -> None:
    """
    Registers all available authorization strategies.

    When adding a new strategy, always register it here.
    """

    # New strategies go here
    AuthorizationStrategiesCatalog.register_item(
        OAuth2Strategy.Strategy, create_oauth2_strategy
    )

    # Print all available strategies for debugging purposes
    names: typing.List[str] = []
    for name, _ in AuthorizationStrategiesCatalog.items():
        names.append(name)
    logging.debug(f"Registered authorization strategies: {'; '.join(names)}")


def create_authorization_strategy(
    comp: BackendComponent,
    svc: Service,
    strategy: str,
    config: typing.Any,
    *,
    user_token: UserToken | None = None,
    auth_token: AuthorizationToken | None = None,
) -> AuthorizationStrategy:
    """
    Creates an authorization strategy using the specified identifier.

    Args:
        comp: The global component.
        svc: The service to use for message sending.
        strategy: The strategy identifier.
        config: The strategy configuration as an arbitrary record.
        user_token: An optional user token.
        auth_token: An optional authorization token.

    Returns:
        The newly created strategy.
    """
    if strategy == "":
        raise RuntimeError("No authorization strategy has been provided")

    strategy_creator = AuthorizationStrategiesCatalog.find_item(strategy)
    if strategy_creator is None:
        raise RuntimeError(f"The authorization strategy '{strategy}' couldn't be found")

    return strategy_creator(
        comp,
        svc,
        config,
        user_token=user_token,
        auth_token=auth_token,
    )
