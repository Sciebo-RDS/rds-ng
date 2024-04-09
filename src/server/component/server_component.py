import typing

from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import ServerRole
from common.py.core.logging import error, info, debug
from common.py.data.storage import StoragePool
from common.py.utils import UnitID

# Make the entire API known
from common.py.api import *


class ServerComponent(BackendComponent):
    """
    The main server component class.
    """

    def __init__(self):
        super().__init__(
            UnitID(ComponentType.INFRASTRUCTURE, ComponentUnit.SERVER),
            ServerRole(),
            module_name=__name__,
        )

        self._add_server_settings()

        self._storage_pool = self._create_storage_pool()

    def run(self) -> None:
        from ..services import (
            create_connectors_service,
            create_projects_service,
            create_resources_service,
            create_session_service,
            create_users_service,
        )

        create_session_service(self)
        create_connectors_service(self)
        create_users_service(self)
        create_projects_service(self)
        create_resources_service(self)

        self._install_network_filters()

        super().run()

    def _add_server_settings(self) -> None:
        from server.settings import get_server_settings

        self.data.config.add_defaults(get_server_settings())

    def _install_network_filters(self) -> None:
        from ..networking.filters import ServerNetworkFilter

        fltr = ServerNetworkFilter(self.data.comp_id)
        self._core.message_bus.network.install_filter(fltr)

    def _create_storage_pool(self) -> StoragePool:
        from ..settings import StorageSettingIDs

        driver = self._data.config.value(StorageSettingIDs.DRIVER)
        debug(f"Creating storage '{driver}'", scope="server")

        try:
            from ..data.storage import StoragePoolsCatalog

            storage_type = StoragePoolsCatalog.find_item(driver)
            if storage_type is None:
                raise RuntimeError(f"The storage driver {driver} couldn't be found")

            storage_pool = typing.cast(StoragePool, storage_type(self.data.config))
            info(f"Created storage: {storage_pool.name}", scope="server")
            return storage_pool
        except Exception as exc:  # pylint: disable=broad-exception-caught
            error(
                f"Unable to create storage: {str(exc)}",
                driver=driver,
            )

            raise exc

    @property
    def storage_pool(self) -> StoragePool:
        return self._storage_pool

    @staticmethod
    def instance() -> "ServerComponent":
        """
        The global ``ServerComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(ServerComponent, BackendComponent.instance())
