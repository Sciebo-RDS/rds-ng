import typing

from common.py.utils import ItemsCatalog
from common.py.utils.config import Configuration

AuthorizationStrategyConfigurationCreator = typing.Callable[
    [Configuration], typing.Dict[str, typing.Any]
]


@ItemsCatalog.define()
class AuthorizationStrategyConfigurationsCatalog(
    ItemsCatalog[AuthorizationStrategyConfigurationCreator]
):
    """
    Global catalog of creator functions for all known authorization strategy configurations.
    """
