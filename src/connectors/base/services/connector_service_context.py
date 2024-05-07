from common.py.services import ClientServiceContext

from ..execution import ConnectorJobsEngine


class ConnectorServiceContext(ClientServiceContext):
    """
    Service context specific to connectors.
    """

    _jobs_engine: ConnectorJobsEngine | None = None

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
