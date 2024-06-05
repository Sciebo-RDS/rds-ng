import typing

from .authorization_strategy import AuthorizationStrategy
from ....component import BackendComponent
from ....services import Service
from ....utils import ItemsCatalog

AuthorizationStrategyCreator = typing.Callable[
    [BackendComponent, Service, typing.Dict[str, typing.Any]], AuthorizationStrategy
]


@ItemsCatalog.define()
class AuthorizationStrategiesCatalog(ItemsCatalog[AuthorizationStrategyCreator]):
    """
    Global catalog of creator functions for all known authorization strategies.
    """
