from common.py.core.logging import LoggerProtocol
from common.py.core.messaging import Command, CommandReplyType
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

        from ..component import ServerComponent

        self._storage_pool = ServerComponent.instance().storage_pool

        self._session_manager = SessionManager()

    def ensure_user(
        self,
        msg: Command,
        reply_type: type[CommandReplyType],
        **kwargs,
    ) -> bool:
        """
        Ensures that a user is authenticated; if not, a default reply (of type `reply_type`) is automatically sent.

        Args:
            msg: The incoming message.
            reply_type: The reply type.
            **kwargs: Arbitrary parameters passed to build the reply.

        Returns:
            Whether a user is currently authenticated.
        """

        if user := self.user is None:
            reply_type.build(
                self.message_builder,
                msg,
                success=False,
                message="No user authenticated",
                **kwargs,
            ).emit()
            return False

        return True

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
        return self._session_manager[self.origin]

    @property
    def session_manager(self) -> SessionManager:
        """
        The global session manager.
        """
        return self._session_manager

    @property
    def storage_pool(self) -> StoragePool:
        """
        The global storage pool.
        """
        return self._storage_pool
