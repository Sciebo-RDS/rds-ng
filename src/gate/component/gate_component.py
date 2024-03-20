from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import NodeRole
from common.py.core.logging import debug, error
from common.py.utils import UnitID

from ..backends import Backend


class GateComponent(BackendComponent):
    """
    The main gate component class.
    """

    def __init__(self):
        super().__init__(
            UnitID(ComponentType.INFRASTRUCTURE, ComponentUnit.GATE),
            NodeRole(),
            module_name=__name__,
        )

        self._backend: Backend | None = None

        self._add_gate_settings()

    def run(self) -> None:
        super().run()

        from ..services import create_gate_service

        create_gate_service(self)

        self._install_network_filters()
        self._mount_backend()

    def _add_gate_settings(self) -> None:
        from gate.settings import get_gate_settings

        self.data.config.add_defaults(get_gate_settings())

    def _install_network_filters(self) -> None:
        from ..networking.gate_filter import GateFilter

        fltr = GateFilter(self.data.comp_id)
        self._core.message_bus.network.install_filter(fltr)

    def _mount_backend(self) -> None:
        from ..settings import BackendSettingIDs

        driver = self.data.config.value(BackendSettingIDs.DRIVER)

        debug(f"Mounting backend driver '{driver}'", scope="gate")

        try:
            from ..backends import BackendsCatalog

            backend_type = BackendsCatalog.find_item(driver)
            if backend_type is None:
                raise RuntimeError(f"The backend driver {driver} couldn't be found")

            self._backend = backend_type(self)
            debug(f"Mounted backend: {self._backend.name}", scope="gate")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            error(
                f"Unable to mount the backend: {str(exc)}",
                driver=driver,
            )

            raise exc
