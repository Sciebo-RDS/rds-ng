import typing

from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import LeafRole
from common.py.utils import UnitID


class ConnectorComponent(BackendComponent):
    """
    The base connector component class.
    """

    def __init__(self, connector_name: str, *, module_name: str):
        super().__init__(
            UnitID(
                ComponentType.INFRASTRUCTURE,
                f"{ComponentUnit.CONNECTOR}:{connector_name}",
            ),
            LeafRole(),
            module_name=module_name,
        )

        self._add_connector_settings()

    def run(self) -> None:
        super().run()

    def _add_connector_settings(self) -> None:
        pass

    @staticmethod
    def instance() -> "ConnectorComponent":
        """
        The global ``ConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(ConnectorComponent, BackendComponent.instance())
