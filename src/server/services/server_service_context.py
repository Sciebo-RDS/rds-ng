from common.py.core.logging import LoggerProtocol, error
from common.py.core.messaging.composers import MessageBuilder
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.data.entities.user import User
from common.py.data.storage import StoragePool
from common.py.services import ServiceContext
from common.py.utils import UnitID
from common.py.utils.config import Configuration

from ..networking.session import SessionManager, Session


class ServerServiceContext(ServiceContext):
    """
    Service context specific to the server.
    """

    def __init__(
        self,
        msg_meta: MessageMetaInformation,
        msg_origin: UnitID,
        msg_builder: MessageBuilder,
        *,
        logger: LoggerProtocol,
        config: Configuration,
    ):
        super().__init__(
            msg_meta, msg_origin, msg_builder, logger=logger, config=config
        )

        self._storage_pool = self._create_storage_pool()

    def _create_storage_pool(self) -> StoragePool:
        from ..settings import StorageSettingIDs

        driver = self._config.value(StorageSettingIDs.DRIVER)
        try:
            from ..data.storage import StoragePoolsCatalog

            storage_type = StoragePoolsCatalog.find_item(driver)
            if storage_type is None:
                raise RuntimeError(f"The storage driver {driver} couldn't be found")

            return storage_type()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            error(
                f"Unable to create storage: {str(exc)}",
                driver=driver,
            )

            raise exc

    @property
    def user(self) -> User | None:
        """
        The user for this session, if any.
        """
        session = self.session
        if session.status == Session.Status.AUTHENTICATED:
            user_id = session.user_token.user_id
            if user := self.storage_pool.user_storage.get(
                user_id
            ):  # User is always created by the users service, so this should always succeed
                return user
        return None

    @property
    def session(self) -> Session:
        """
        The session for this context.
        """
        return self.session_manager[self.origin]

    @property
    def session_manager(self) -> SessionManager:
        """
        The global session manager.
        """
        return SessionManager()

    @property
    def storage_pool(self) -> StoragePool:
        """
        The global storage pool.
        """
        return self._storage_pool
