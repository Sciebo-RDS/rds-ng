from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import ServerRole
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

    def run(self) -> None:
        from ..services import (
            create_session_service,
            create_connectors_service,
            create_users_service,
        )

        create_session_service(self)
        create_connectors_service(self)
        create_users_service(self)

        self._install_network_filters()

        super().run()

    def _add_server_settings(self) -> None:
        from server.settings import get_server_settings

        self.data.config.add_defaults(get_server_settings())

    def _install_network_filters(self) -> None:
        from ..networking.filters import ServerNetworkFilter

        fltr = ServerNetworkFilter(self.data.comp_id)
        self._core.message_bus.network.install_filter(fltr)
