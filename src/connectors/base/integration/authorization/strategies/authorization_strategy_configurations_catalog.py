import typing

from common.py.utils import ItemsCatalog
from common.py.utils.config import Configuration

from .authorization_strategy_configurations import AuthorizationStrategyConfiguration

AuthorizationStrategyConfigurationCreator = typing.Callable[
    [Configuration], AuthorizationStrategyConfiguration
]


@ItemsCatalog.define()
class AuthorizationStrategyConfigurationsCatalog(
    ItemsCatalog[AuthorizationStrategyConfigurationCreator]
):
    """
    Global catalog of creator functions for all known authorization strategy configurations.
    """
