import typing

from ...base.component import ConnectorComponent


class DataverseConnectorComponent(ConnectorComponent):
    """
    The Dataverse connector component class.
    """

    def __init__(self):
        from ..execution import DataverseJobExecutor, DataverseRequestsHandler

        super().__init__(
            executor_type=DataverseJobExecutor,
            handler_type=DataverseRequestsHandler,
            module_name=__name__,
        )

    @staticmethod
    def instance() -> "DataverseConnectorComponent":
        """
        The global ``DataverseConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(DataverseConnectorComponent, ConnectorComponent.instance())
