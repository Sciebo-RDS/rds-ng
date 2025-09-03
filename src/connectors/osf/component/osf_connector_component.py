import typing

from ..execution import OSFRequestsHandler
from ...base.component import ConnectorComponent


class OSFConnectorComponent(ConnectorComponent):
    """
    The OSF connector component class.
    """

    def __init__(self):
        from ..execution import OSFJobExecutor

        super().__init__(
            executor_type=OSFJobExecutor,
            handler_type=OSFRequestsHandler,
            module_name=__name__,
        )

    @staticmethod
    def instance() -> "OSFConnectorComponent":
        """
        The global ``OSFConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(OSFConnectorComponent, ConnectorComponent.instance())
