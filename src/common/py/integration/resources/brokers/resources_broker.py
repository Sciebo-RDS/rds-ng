import abc

from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.resource import ResourcesList
from ....services import Service


class ResourcesBroker(abc.ABC):
    """
    Base class for all resources brokers.

    Notes:
        Brokers report errors through raising exceptions (usually *RuntimeError*).
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        broker: str,
        *,
        auth_token: AuthorizationToken | None = None
    ):
        """
        Args:
            comp: The global component.
            broker: The broker identifier.
        """
        # TODO: Use svc+auth_token to create strategy
        self._component = comp

        self._broker = broker

    @abc.abstractmethod
    def list_resources(
        self,
        root: str,
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> ResourcesList: ...

    def _resolve_root_path(self, root: str, base_root: str = "") -> str:
        root_path = root if root != "" else base_root
        if root_path == "":
            from ....settings.integration_setting_ids import IntegrationSettingIDs

            root_path = self._component.data.config.value(
                IntegrationSettingIDs.DEFAULT_ROOT_PATH
            )
        return root_path

    @property
    def broker(self) -> str:
        """
        The broker identifier.
        """
        return self._broker
