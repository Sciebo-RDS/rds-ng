import threading
import typing
from enum import Enum, auto

from common.py.data.entities.user import UserToken
from common.py.utils import UnitID

SessionID = UnitID
SessionData = typing.Dict[str, typing.Any]


class Session:
    """
    Manages the data of a single session.

    Notes:
        Values are accessed and handled like dictionary items.
    """

    class Status(Enum):
        """
        The state of a session.
        """

        DEFAULT = auto()
        AUTHENTICATED = auto()

    def __init__(self, session_id: UnitID):
        self._session_id = session_id

        self._user_token: UserToken | None = None

        self._data: SessionData = {}
        self._lock = threading.RLock()

    def authenticate(self, user_token: UserToken) -> bool:
        """
        Assigns a user token to this session.

        Args:
            user_token: The user token.
        """
        if user_token.user_id == "":
            return False

        self._user_token = user_token
        return True

    def __getitem__(self, key: str) -> typing.Any:
        """
        Retrieves a data value stored in this session.

        Args:
            key: The value name.

        Returns:
            The stored value or the `None` otherwise.
        """
        with self._lock:
            if key not in self._data:
                self._data[key] = None
            return self._data[key]

    def __setitem__(self, key: str, value: typing.Any) -> None:
        """
        Stores a data value in this session.

        Args:
            key: The value name.
            value: The value.
        """
        with self._lock:
            self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Checks if a certain value is stored in this session.

        Args:
            key: The value name.
        """
        with self._lock:
            return key in self._data

    def __delitem__(self, key: str) -> None:
        """
        Clears a single data entry of this session.

        Args:
            key: The value name.
        """
        with self._lock:
            if key in self._data:
                del self._data[key]

    @property
    def status(self) -> Status:
        with self._lock:
            if self._user_token is not None and self._user_token.user_id != "":
                return Session.Status.AUTHENTICATED

            return Session.Status.DEFAULT

    @property
    def session_id(self) -> UnitID:
        """
        The ID of this session.
        """
        return self._session_id

    @property
    def user_token(self) -> UserToken | None:
        """
        The current authentication user token, if any.
        """
        return self._user_token
