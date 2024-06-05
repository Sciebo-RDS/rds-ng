import abc
import typing

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

    def _get_config_value(self, key: str, default: typing.Any) -> typing.Any:
        from ....utils.config import SettingID

        setting_id = SettingID(f"authorization.{self._strategy}", key)
        return self._component.data.config.value_with_default(setting_id, default)

    @property
    def strategy(self) -> str:
        return self._strategy
