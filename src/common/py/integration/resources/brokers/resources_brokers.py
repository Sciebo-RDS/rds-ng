import typing

from .filesystem import FilesystemBroker, create_filesystem_broker
from .resources_broker import ResourcesBroker
from .resources_brokers_catalog_catalog import ResourcesBrokersCatalog
from .webdav import WebdavBroker, create_webdav_broker
from ....component import BackendComponent
from ....core import logging
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.user import UserToken
from ....services import Service


def register_resources_brokers() -> None:
    """
    Registers all available resources brokers.

    When adding a new broker, always register it here.
    """

    # New brokers go here
    ResourcesBrokersCatalog.register_item(
        FilesystemBroker.Broker, create_filesystem_broker
    )
    ResourcesBrokersCatalog.register_item(WebdavBroker.Broker, create_webdav_broker)

    # Print all available brokers for debugging purposes
    names: typing.List[str] = []
    for name, _ in ResourcesBrokersCatalog.items():
        names.append(name)
    logging.debug(f"Registered resources brokers: {'; '.join(names)}")


def create_resources_broker(
    comp: BackendComponent,
    svc: Service,
    broker: str,
    config: typing.Any,
    *,
    user_token: UserToken,
    auth_token: AuthorizationToken | None = None,
) -> ResourcesBroker:
    """
    Creates a resources broker using the specified identifier.

    Args:
        comp: The global component.
        svc: The service used for message sending.
        broker: The broker identifier.
        config: The broker configuration as an arbitrary record.
        user_token: The user token.
        auth_token: An authorization token (can be **None**).

    Returns:
        The newly created broker.
    """
    if broker == "":
        raise RuntimeError("No resources broker has been provided")

    broker_creator = ResourcesBrokersCatalog.find_item(broker)
    if broker_creator is None:
        raise RuntimeError(f"The resources broker '{broker}' couldn't be found")

    return broker_creator(comp, svc, config, user_token, auth_token)
