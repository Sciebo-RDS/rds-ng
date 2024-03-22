from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import ServerRole
from common.py.core.logging import debug, error
from common.py.data.storage import StoragePool
from common.py.utils import UnitID


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

        self._storage_pool: StoragePool | None = None

        self._add_server_settings()

    def run(self) -> None:
        from ..services import create_session_service

        create_session_service(self)

        self._install_network_filters()
        self._mount_storage()

        super().run()

    def _add_server_settings(self) -> None:
        from server.settings import get_server_settings

        self.data.config.add_defaults(get_server_settings())

    def _install_network_filters(self) -> None:
        from ..networking.filters import ServerNetworkFilter

        fltr = ServerNetworkFilter(self.data.comp_id)
        self._core.message_bus.network.install_filter(fltr)

    def _mount_storage(self) -> None:
        from ..settings import StorageSettingIDs

        driver = self.data.config.value(StorageSettingIDs.DRIVER)

        debug(f"Mounting storage driver '{driver}'", scope="server")

        try:
            from ..data.storage import StoragePoolsCatalog

            storage_type = StoragePoolsCatalog.find_item(driver)
            if storage_type is None:
                raise RuntimeError(f"The storage driver {driver} couldn't be found")

            self._storage_pool = storage_type()
            debug(f"Mounted storage: {self._storage_pool.name}", scope="server")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            error(
                f"Unable to mount storage: {str(exc)}",
                driver=driver,
            )

            raise exc
