import typing

from common.py.component import BackendComponent, ComponentType, ComponentUnit
from common.py.component.roles import LeafRole
from common.py.utils import UnitID

from ..execution import (
    ConnectorJobExecutorType,
    ConnectorJobsEngine,
    ConnectorRequestsHandler,
    ConnectorRequestsHandlerType,
)
from .connector_information import ConnectorInformation


class ConnectorComponent(BackendComponent):
    """
    The base connector component class.
    """

    def __init__(
        self,
        *,
        executor_type: type[ConnectorJobExecutorType],
        handler_type: type[ConnectorRequestsHandlerType],
        module_name: str,
    ):
        connector_info = ConnectorInformation()

        super().__init__(
            UnitID(
                ComponentType.INFRASTRUCTURE,
                f"{ComponentUnit.CONNECTOR}:{connector_info.connector_id}",
            ),
            connector_info.name,
            LeafRole(),
            module_name=module_name,
        )

        self._add_connector_settings()

        self._connector_info = connector_info

        self._jobs_engine = ConnectorJobsEngine(executor_type=executor_type)
        self._requests_handler_type = handler_type

    def run(self) -> None:
        from ..data.entities.connector.categories import register_connector_categories
        from ..integration.authorization.strategies import (
            register_authorization_strategy_configurations,
        )
        from ..services import (
            ConnectorServiceContext,
            create_authorization_service,
            create_connector_service,
            create_projects_service,
            create_project_jobs_service,
        )

        # Assign the global jobs engine and requests handler to the service context
        ConnectorServiceContext.set_jobs_engine(self._jobs_engine)
        ConnectorServiceContext.set_requests_handler_type(self._requests_handler_type)

        # Register global items
        register_connector_categories()
        register_authorization_strategy_configurations()

        # Create connector-specific services
        create_connector_service(self)
        create_authorization_service(self)
        create_projects_service(self)
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
