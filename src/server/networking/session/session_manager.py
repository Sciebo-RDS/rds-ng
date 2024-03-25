import threading
import typing

from .session import SessionID, Session


class SessionManager:
    """
    Manages in-memory sessions.
    """

    _sessions: typing.Dict[SessionID, Session] = {}
    _lock = threading.RLock()

    def __getitem__(self, session_id: SessionID) -> Session:
        """
        Gets the session for the given id; if none exists yet, a new one is created.

        To use the manager, access session using the index `[]` operator; to delete a session, use the `del` operator;
        check for existence of a session using the `in` operator with a session ID.

        Args:
            session_id: The session ID.

        Returns:
            The session object.
        """
        with SessionManager._lock:
            if session_id not in SessionManager._sessions:
                SessionManager._sessions[session_id] = Session(session_id)
            return SessionManager._sessions[session_id]

    def __delitem__(self, session_id: SessionID) -> None:
        """
        Removes an existing session.

        Args:
            session_id: The session ID.
        """
        with SessionManager._lock:
            if session_id in SessionManager._sessions:
                del SessionManager._sessions[session_id]

    def __contains__(self, session_id: SessionID) -> bool:
        """
        Checks whether a session for the given ID exists.

        Args:
            session_id: The session ID.
        """
        with SessionManager._lock:
            return session_id in SessionManager._sessions
