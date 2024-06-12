import typing

from .resources_broker import ResourcesBroker
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....services import Service
from ....utils import ItemsCatalog

ResourcesBrokerCreator = typing.Callable[
    [BackendComponent, Service, typing.Any, AuthorizationToken | None],
    ResourcesBroker,
]


@ItemsCatalog.define()
class ResourcesBrokersCatalog(ItemsCatalog[ResourcesBrokerCreator]):
    """
    Global catalog of creator functions for all known resources brokers.
    """
