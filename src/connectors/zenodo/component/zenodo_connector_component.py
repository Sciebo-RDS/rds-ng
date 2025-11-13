import typing

from ...base.component import ConnectorComponent


class ZenodoConnectorComponent(ConnectorComponent):
    """
    The Zenodo connector component class.
    """

    def __init__(self):
        from ..execution import ZenodoJobExecutor, ZenodoRequestsHandler

        super().__init__(
            executor_type=ZenodoJobExecutor,
            handler_type=ZenodoRequestsHandler,
            module_name=__name__,
        )

    @staticmethod
    def instance() -> "ZenodoConnectorComponent":
        """
        The global ``ZenodoConnectorComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(ZenodoConnectorComponent, ConnectorComponent.instance())
