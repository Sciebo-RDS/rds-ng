from common.py.component import BackendComponent
from common.py.services import ClientServiceContext, Service

from ..execution import (
    ConnectorJobsEngine,
    ConnectorRequestsHandler,
    ConnectorRequestsHandlerType,
)


class ConnectorServiceContext(ClientServiceContext):
    """
    Service context specific to connectors.
    """

    _jobs_engine: ConnectorJobsEngine | None = None
    _requests_handler_type: type[ConnectorRequestsHandlerType] | None = None

    @staticmethod
    def set_jobs_engine(engine: ConnectorJobsEngine) -> None:
        """
        Sets the global connector jobs engine.

        Args:
            engine: The connector jobs engine.
        """
        ConnectorServiceContext._jobs_engine = engine

    @property
    def jobs_engine(self) -> ConnectorJobsEngine:
        """
        The connector jobs engine.

        Raises:
            RuntimeError: If the job engine hasn't been set.
        """
        if ConnectorServiceContext._jobs_engine is None:
            raise RuntimeError(
                "Tried to access the jobs engine prior to its assignment"
            )

        return ConnectorServiceContext._jobs_engine

    @staticmethod
    def set_requests_handler_type(
        handler_type: type[ConnectorRequestsHandlerType],
    ) -> None:
        """
        Sets the global connector requests handler.

        Args:
            handler_type: The connector requests handler type.
        """
        ConnectorServiceContext._requests_handler_type = handler_type

    def requests_handler(
        self, comp: BackendComponent, svc: Service
    ) -> ConnectorRequestsHandler:
        """
        Creates a new connector requests handler.

        Args:
            comp: The main component.
            svc: The underlying service.

        Raises:
            RuntimeError: If the requests handler hasn't been set.
        """
        from ..component import ConnectorComponent

        if ConnectorServiceContext.set_requests_handler_type is None:
            raise RuntimeError(
                "Tried to create a requests handler without an assigned type"
            )

        return ConnectorServiceContext._requests_handler_type(
            comp, svc, auth_channel=self.remote_channel
        )
