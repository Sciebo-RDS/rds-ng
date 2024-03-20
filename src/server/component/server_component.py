from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import ServerRole
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

        self._add_server_settings()

    def run(self) -> None:
        super().run()

        from ..services import create_server_service

        create_server_service(self)

    def _add_server_settings(self) -> None:
        from server.settings import get_server_settings

        self.data.config.add_defaults(get_server_settings())
