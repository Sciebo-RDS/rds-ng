import typing

from common.py.integration.authorization.strategies import (
    OAuth2Strategy,
    OAuth2Configuration,
)


def get_default_strategy_configuration(strategy: str) -> typing.Any:
    """
    Creates a default configuration for all known authorization strategies.

    Args:
        strategy: The strategy identifier.

    Returns:
        The default configuration, or **None** if the strategy is unknown.
    """
    if strategy == OAuth2Strategy.Strategy:
        return OAuth2Configuration()

    return None
