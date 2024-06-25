import typing

from common.py.core import logging
from common.py.integration.authorization.strategies import OAuth2Strategy
from common.py.utils.config import Configuration

from .authorization_strategy_configurations_catalog import (
    AuthorizationStrategyConfigurationsCatalog,
)
from .oauth2 import get_oauth2_strategy_configuration


def register_authorization_strategy_configurations() -> None:
    """
    Registers all available authorization strategy configurations.

    When adding a new strategy, always register its configuration here, too.
    """

    # New strategy configurations go here
    AuthorizationStrategyConfigurationsCatalog.register_item(
        OAuth2Strategy.Strategy, get_oauth2_strategy_configuration
    )

    # Print all available strategies for debugging purposes
    names: typing.List[str] = []
    for name, _ in AuthorizationStrategyConfigurationsCatalog.items():
        names.append(name)
    logging.debug(
        f"Registered authorization strategy configurations: {'; '.join(names)}"
    )


def create_authorization_strategy_configuration(
    strategy: str,
    config: Configuration,
) -> typing.Dict[str, typing.Any]:
    """
    Creates an authorization strategy configuration using the specified identifier.

    Args:
        strategy: The strategy identifier.
        config: The global component configuration.

    Returns:
        The newly created strategy configuration.
    """
    if strategy == "":
        raise RuntimeError("No authorization strategy has been provided")

    config_creator = AuthorizationStrategyConfigurationsCatalog.find_item(strategy)
    if config_creator is None:
        raise RuntimeError(f"The authorization strategy '{strategy}' couldn't be found")

    return config_creator(config)
