import typing

from .oauth2.oauth2_strategy import OAuth2Strategy, OAuth2StrategyConfiguration


def get_authorization_strategy_configuration(strategy: str) -> typing.Any:
    """
    Creates a default configuration for all known authorization strategies.

    Args:
        strategy: The strategy identifier.

    Returns:
        The default configuration, or **None** if the strategy is unknown.
    """
    if strategy == OAuth2Strategy.Strategy:
        return OAuth2StrategyConfiguration()

    return None
