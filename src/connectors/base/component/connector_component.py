import typing

from common.py.component import (
    ComponentType,
    ComponentUnit,
    BackendComponent,
)
from common.py.component.roles import LeafRole
from common.py.utils import UnitID

from .connector_information import ConnectorInformation
from ..execution import ConnectorJobsEngine, ConnectorJobExecutorType


class ConnectorComponent(BackendComponent):
    """
    The base connector component class.
    """

    def __init__(
        self,
        connector_id: str,
        *,
        executor_type: type[ConnectorJobExecutorType],
        module_name: str,
    ):
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

        self._jobs_engine = ConnectorJobsEngine(executor_type=executor_type)

    def run(self) -> None:
        from ..data.entities.connector.categories import register_connector_categories
        from ..services import (
            create_connector_service,
            create_authorization_service,
            create_project_jobs_service,
            ConnectorServiceContext,
        )

        # Assign the global jobs engine to the service context
        ConnectorServiceContext.set_jobs_engine(self._jobs_engine)

        # Register global items
        register_connector_categories()

        # Create connector-specific services
        create_connector_service(self)
        create_authorization_service(self)
        create_project_jobs_service(self)

        super().run()

    def _add_connector_settings(self) -> None:
        from ..settings import get_connector_settings

        self.data.config.add_defaults(get_connector_settings())

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
