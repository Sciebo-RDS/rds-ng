import threading
import typing

from common.py.data.entities.user import UserID

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

    def find_user_sessions(self, user_id: UserID) -> typing.List[Session]:
        """
        Finds all sessions associated with the user ID. Since a single user can be logged in for several sessions, a list of all these is returned.

        Args:
            user_id: The user ID.

        Returns:
            All associated sessions.
        """
        with SessionManager._lock:
            sessions: typing.List[Session] = []
            for _, session in SessionManager._sessions.items():
                if session.user_token and session.user_token.user_id == user_id:
                    sessions.append(session)
            return sessions
