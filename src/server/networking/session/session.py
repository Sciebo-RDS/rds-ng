import threading
import typing
from enum import Enum, auto

from common.py.data.entities.resource import ResourcesBrokerToken
from common.py.data.entities.user import UserToken
from common.py.utils import UnitID, generate_random_string

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
        self._user_origin: UnitID | None = None

        self._broker_token: ResourcesBrokerToken | None = None

        self._fingerprint = generate_random_string(32)

        self._data: SessionData = {}
        self._lock = threading.RLock()

    def authenticate(self, user_token: UserToken, user_origin: UnitID) -> bool:
        """
        Assigns a user token to this session.

        Args:
            user_token: The user token.
            user_origin: The origin of the user.
        """
        with self._lock:
            if user_token.user_id == "":
                return False

            self._user_token = user_token
            self._user_origin = user_origin
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
        with self._lock:
            return self._session_id

    @property
    def user_token(self) -> UserToken | None:
        """
        The current authentication user token, if any.
        """
        with self._lock:
            return self._user_token

    @property
    def user_origin(self) -> UnitID | None:
        """
        The origin of the currently authenticated user, if any.
        """
        with self._lock:
            return self._user_origin

    @property
    def broker_token(self) -> ResourcesBrokerToken | None:
        """
        The assigned broker token.
        """
        with self._lock:
            return self._broker_token

    @broker_token.setter
    def broker_token(self, value: ResourcesBrokerToken | None) -> None:
        self._broker_token = value

    @property
    def fingerprint(self) -> str:
        """
        The (random) fingerprint of the user's session.
        """
        with self._lock:
            return self._fingerprint
