import typing

from common.py.component import BackendComponent, ComponentType, ComponentUnit
from common.py.component.roles import LeafRole
from common.py.utils import UnitID

from ..execution import ConnectorJobExecutorType, ConnectorJobsEngine
from .connector_information import ConnectorInformation


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
        from ..integration.authorization.strategies import (
            register_authorization_strategy_configurations,
        )
        from ..services import (
            ConnectorServiceContext,
            create_authorization_service,
            create_connector_service,
            create_project_jobs_service,
        )

        # Assign the global jobs engine to the service context
        ConnectorServiceContext.set_jobs_engine(self._jobs_engine)

        # Register global items
        register_connector_categories()
        register_authorization_strategy_configurations()

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

    @property
    def metadata_profile_name(self) -> str:
        """
        The name of the metadata profile.
        """
        return self.connector_info.metadata_profile.metadata.id[0]

    @staticmethod
    def instance() -> "ConnectorComponent":
        """
        The global ``ConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(ConnectorComponent, BackendComponent.instance())
