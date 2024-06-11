import abc

from ....component import BackendComponent
from ....data.entities.resource import ResourcesList


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
