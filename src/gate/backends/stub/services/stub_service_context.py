import typing

from common.py.core.logging import LoggerProtocol
from common.py.core.messaging.composers import MessageBuilder
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.data.entities.user import UserSettings
from common.py.data.storage import StoragePool
from common.py.utils import UnitID
from common.py.utils.config import Configuration

from ....services import GateServiceContext


class StubServiceContext(GateServiceContext):
    """
    Service context specific to the stub backend.
    """

    # A simple global object to store user settings
    user_settings: typing.Dict[str, UserSettings] = {}

    def __init__(
        self,
        msg_meta: MessageMetaInformation,
        msg_origin: UnitID,
        msg_builder: MessageBuilder,
        *,
        logger: LoggerProtocol,
        config: Configuration,
    ):
        from ....data.storage.memory import MemoryStoragePool
        from ....data.storage.session import SessionStorage

        super().__init__(
            msg_meta, msg_origin, msg_builder, logger=logger, config=config
        )

        # The user token is sent by the client and stored in the session of the user
        self._user_token = SessionStorage().get_data(
            msg_origin, "user-token", "default_user"
        )

        # Connectors are global for all users, projects are specific to each user
        self._storage_pool = MemoryStoragePool(
            project_storage_id=f"user:{self._user_token}"
        )

    @property
    def user_token(self) -> str:
        """
        The user token.
        """
        return self._user_token

    @property
    def storage_pool(self) -> StoragePool:
        """
        The storage pool used by the stub backend.
        """
        return self._storage_pool
