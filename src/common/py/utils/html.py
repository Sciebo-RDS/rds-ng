from enum import IntEnum


class RedirectionTarget(IntEnum):
    """
    Targets for website redirections.
    """
    CURRENT = 0
    BLANK = 1
