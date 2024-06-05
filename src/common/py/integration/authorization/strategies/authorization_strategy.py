import abc

from ....component import BackendComponent
from ....services import Service


class AuthorizationStrategy(abc.ABC):
    """
    Base class for all authorization strategies.
    """

    def __init__(self, comp: BackendComponent, svc: Service, strategy: str):
        """
        Args:
            comp: The global component.
            svc: The service used to send messages through.
            strategy: The strategy identifier.
        """
        self._component = comp
        self._service = svc

        self._strategy = strategy

    @property
    def strategy(self) -> str:
        return self._strategy
