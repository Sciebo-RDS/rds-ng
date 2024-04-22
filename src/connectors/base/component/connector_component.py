import typing

from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import LeafRole
from common.py.utils import UnitID

from .connector_information import ConnectorInformation


class ConnectorComponent(BackendComponent):
    """
    The base connector component class.
    """

    def __init__(self, connector_id: str, *, module_name: str):
        super().__init__(
            UnitID(
                ComponentType.INFRASTRUCTURE,
                f"{ComponentUnit.CONNECTOR}:{connector_id}",
            ),
            LeafRole(),
            module_name=module_name,
        )

        self._add_connector_settings()

        self._connector_info = ConnectorInformation(connector_id)

    def run(self) -> None:
        from ..data.entities.connector.categories import register_connector_categories
        from ..services.connector_service import create_connector_service

        # Register global items
        register_connector_categories()

        # Create connector-specific services
        create_connector_service(self)

        super().run()

    def _add_connector_settings(self) -> None:
        pass

    @property
    def connector_info(self) -> ConnectorInformation:
        """
        The global connector information.
        """
        return self._connector_info

    @staticmethod
    def instance() -> "ConnectorComponent":
        """
        The global ``ConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(ConnectorComponent, BackendComponent.instance())
