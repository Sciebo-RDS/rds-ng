import typing

from ..execution import StubRequestsHandler
from ...base.component import ConnectorComponent


class StubConnectorComponent(ConnectorComponent):
    """
    The stub connector component class.
    """

    def __init__(self):
        from ..execution import StubJobExecutor

        super().__init__(
            executor_type=StubJobExecutor,
            handler_type=StubRequestsHandler,
            module_name=__name__,
        )

    @staticmethod
    def instance() -> "StubConnectorComponent":
        """
        The global ``StubConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(StubConnectorComponent, ConnectorComponent.instance())
