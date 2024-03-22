import threading
import typing

from common.py.utils import UnitID

SessionID = UnitID
SessionData = typing.Dict[str, typing.Any]
SessionDataType = typing.TypeVar("SessionDataType")


class SessionStorage:
    """
    Manages in-memory session storage (i.e., a per-session key-value storage).
    """

    GLOBAL_SESSION: SessionID = UnitID("__session__", "__global__")

    _sessions: typing.Dict[SessionID, SessionData] = {}
    _lock = threading.RLock()

    @staticmethod
    def get_data(
        session: SessionID, key: str, default: SessionDataType = None
    ) -> SessionDataType:
        """
        Retrieves a value of a session.

        Args:
            session: The session ID.
            key: The value name.
            default: A default fallback value.

        Returns:
            The stored value or the default value otherwise.
        """
        with SessionStorage._lock:
            data = SessionStorage._session_data(session)
            if key not in data:
                data[key] = default
            return typing.cast(SessionDataType, data[key])

    @staticmethod
    def set_data(session: SessionID, key: str, value: SessionDataType) -> None:
        """
        Stores a value for a session.

        Args:
            session: The session ID.
            key: The value name.
            value: The value.
        """
        with SessionStorage._lock:
            data = SessionStorage._session_data(session)
            data[key] = value

    @staticmethod
    def has_data(session: SessionID, key: str) -> bool:
        """
        Checks if a certain value is stored for the session.

        Args:
            session: The session ID.
            key: The value name.
        """
        with SessionStorage._lock:
            data = SessionStorage._session_data(session)
            return key in data

    @staticmethod
    def clear_data(session: SessionID, key: str) -> None:
        """
        Clears a single data entry of a session.

        Args:
            session: The session ID.
            key: The value name.
        """
        with SessionStorage._lock:
            data = SessionStorage._session_data(session)
            if key in data:
                del data[key]

    @staticmethod
    def clear_session(session: SessionID) -> None:
        """
        Clears data of a session.

        Args:
            session: The session ID.
        """
        with SessionStorage._lock:
            if session in SessionStorage._sessions:
                SessionStorage._sessions.pop(session)

    @staticmethod
    def _session_data(session: SessionID) -> SessionData:
        if session not in SessionStorage._sessions:
            SessionStorage._sessions[session] = {}
        return SessionStorage._sessions[session]
