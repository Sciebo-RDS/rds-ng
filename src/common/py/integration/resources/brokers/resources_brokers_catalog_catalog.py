import typing

from .resources_broker import ResourcesBroker
from ....component import BackendComponent
from ....utils import ItemsCatalog

ResourcesBrokerCreator = typing.Callable[
    [BackendComponent, typing.Any], ResourcesBroker
]


@ItemsCatalog.define()
class ResourcesBrokersCatalog(ItemsCatalog[ResourcesBrokerCreator]):
    """
    Global catalog of creator functions for all known resources brokers.
    """
