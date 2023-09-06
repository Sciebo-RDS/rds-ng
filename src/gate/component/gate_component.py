from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import NodeRole
from common.py.core.logging import debug, error
from common.py.services import Service
from common.py.utils import UnitID


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

        self._backend: Service | None = None

        self._add_gate_settings()

    def run(self) -> None:
        super().run()

        # Install a network filter to ensure that only properly directed messages pass the gate
        from ..networking.gate_filter import GateFilter

        self._core.message_bus.network.install_filter(GateFilter(self.data.comp_id))

        # Mount the backend using the configured driver
        from ..settings import BackendSettingIDs

        driver = self.data.config.value(BackendSettingIDs.DRIVER)
        try:
            self._backend = self._mount_backend(driver)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            error(
                f"Unable to mount the backend: {str(exc)}",
                driver=driver,
            )

            from .exit_codes import EXIT_MOUNT_BACKEND_FAILED

            exit(EXIT_MOUNT_BACKEND_FAILED)

    def _add_gate_settings(self):
        from gate.settings.gate_settings import get_gate_settings

        self.data.config.add_defaults(get_gate_settings())

    def _mount_backend(self, driver: str) -> Service:
        debug(f"Mounting backend driver '{driver}'...", scope="gate")

        from ..backends import BackendsCatalog

        creator = BackendsCatalog.find_item(driver)
        if creator is None:
            raise RuntimeError(f"The backend driver {driver} couldn't be found")

        return creator(self)
