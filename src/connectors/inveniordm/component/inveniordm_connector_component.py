import typing

from ...base.component import ConnectorComponent


class InvenioRDMConnectorComponent(ConnectorComponent):
    """
    The InvenioRDM connector component class.
    """

    def __init__(self):
        from ..execution import InvenioRDMJobExecutor, InvenioRDMRequestsHandler

        super().__init__(
            executor_type=InvenioRDMJobExecutor,
            handler_type=InvenioRDMRequestsHandler,
            module_name=__name__,
        )

    @staticmethod
    def instance() -> "InvenioRDMConnectorComponent":
        """
        The global ``InvenioRDMConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(InvenioRDMConnectorComponent, ConnectorComponent.instance())
