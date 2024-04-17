import typing

from ...base.component import ConnectorComponent


class StubConnectorComponent(ConnectorComponent):
    """
    The stub connector component class.
    """

    def __init__(self):
        super().__init__(
            "stub",
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
