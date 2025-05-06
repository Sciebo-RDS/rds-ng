from enum import IntEnum


class AuthorizationState(IntEnum):
    """
    The state of an authorization.
    """

    PENDING = -1
    NOT_AUTHORIZED = 0
    AUTHORIZED = 1
