import threading
import typing

from common.py.utils import UnitID

SessionID = UnitID
SessionData = typing.Dict[str, typing.Any]


class SessionStorage:
    """
    Manages in-memory session storage (i.e., a per-session key-value storage).

    Notes:
        The data is shared among all instances of this class.
    """

    _sessions: typing.Dict[SessionID, SessionData] = {}
    _lock = threading.RLock()

    def get_data(
        self, session: SessionID, key: str, default: typing.Any = None
    ) -> typing.Any:
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
            data = self._session_data(session)
            return data[key] if key in data else default

    def set_data(self, session: SessionID, key: str, value: typing.Any) -> None:
        """
        Stores a value for a session.

        Args:
            session: The session ID.
            key: The value name.
            value: The value.
        """
        with SessionStorage._lock:
            data = self._session_data(session)
            data[key] = value

    def has_data(self, session: SessionID, key: str) -> bool:
        """
        Checks if a certain value is stored for the session.

        Args:
            session: The session ID.
            key: The value name.
        """
        with SessionStorage._lock:
            data = self._session_data(session)
            return key in data

    def clear_data(self, session: SessionID) -> None:
        """
        Clears data of a session.

        Args:
            session: The session ID.
        """
        with SessionStorage._lock:
            if session in self._sessions:
                self._sessions.pop(session)

    def _session_data(self, session: SessionID) -> SessionData:
        if session not in SessionStorage._sessions:
            SessionStorage._sessions[session] = {}
        return SessionStorage._sessions[session]
