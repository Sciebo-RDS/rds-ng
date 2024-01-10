import abc
import typing

from common.py.component import BackendComponent
from common.py.services import Service


class Backend(abc.ABC):
    """
    Base class for all backends.
    """

    def __init__(
        self, comp: BackendComponent, name: str, services: typing.List[Service]
    ):
        """
        Args:
            comp: The backend component.
            name: The name of the backend.
            services: A list of all services belonging to this backend.
        """
        self._comp = comp

        self._name = name

        self._services = services

    @property
    def name(self) -> str:
        """
        The name of this backend.
        """
        return self._name

    @property
    def services(self) -> typing.List[Service]:
        """
        List of all services belonging to this backend.
        """
        return self._services
