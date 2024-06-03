from enum import IntEnum


class AuthorizationState(IntEnum):
    """
    The state of an authorization.
    """

    NOT_AUTHORIZED = 0
    AUTHORIZED = 1
