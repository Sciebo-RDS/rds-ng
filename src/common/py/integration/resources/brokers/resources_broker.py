import abc

from common.py.component import BackendComponent


class ResourcesBroker(abc.ABC):
    """
    Base class for all resources brokers.

    Notes:
        Brokers report errors through raising exceptions (usually *RuntimeError*).
    """

    def __init__(self, comp: BackendComponent, broker: str):
        """
        Args:
            comp: The global component.
            broker: The broker identifier.
        """
        self._component = comp

        self._broker = broker

    @property
    def broker(self) -> str:
        """
        The broker identifier.
        """
        return self._broker
