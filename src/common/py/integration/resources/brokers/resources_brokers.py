import typing

from .filesystem import FilesystemBroker, create_filesystem_broker
from .resources_broker import ResourcesBroker
from .resources_brokers_catalog_catalog import ResourcesBrokersCatalog
from ....component import BackendComponent
from ....core import logging


def register_resources_brokers() -> None:
    """
    Registers all available resources brokers.

    When adding a new broker, always register it here.
    """

    # New brokers go here
    ResourcesBrokersCatalog.register_item(
        FilesystemBroker.Broker, create_filesystem_broker
    )

    # Print all available brokers for debugging purposes
    names: typing.List[str] = []
    for name, _ in ResourcesBrokersCatalog.items():
        names.append(name)
    logging.debug(f"Registered resources brokers: {'; '.join(names)}")


def create_resources_broker(
    comp: BackendComponent,
    broker: str,
    config: typing.Any,
) -> ResourcesBroker:
    """
    Creates a resources broker using the specified identifier.

    Args:
        comp: The global component.
        broker: The broker identifier.
        config: The broker configuration as an arbitrary record.

    Returns:
        The newly created broker.
    """
    if broker == "":
        raise RuntimeError("No resources broker has been provided")

    broker_creator = ResourcesBrokersCatalog.find_item(broker)
    if broker_creator is None:
        raise RuntimeError(f"The resources broker '{broker}' couldn't be found")

    return broker_creator(comp, config)
