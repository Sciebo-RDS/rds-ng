import typing

from .authorization_strategy import AuthorizationStrategy
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.user import UserToken
from ....services import Service
from ....utils import ItemsCatalog

AuthorizationStrategyCreator = typing.Callable[
    [
        BackendComponent,
        Service,
        UserToken | None,
        AuthorizationToken | None,
    ],
    AuthorizationStrategy,
]


@ItemsCatalog.define()
class AuthorizationStrategiesCatalog(ItemsCatalog[AuthorizationStrategyCreator]):
    """
    Global catalog of creator functions for all known authorization strategies.
    """
