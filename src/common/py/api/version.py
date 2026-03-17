from enum import auto, IntEnum

from semantic_version import Version

API_PROTOCOL_VERSION: Version = Version("3.0.0")


class ProtocolCompatibility(IntEnum):
    """
    Compatibility degrees.
    """

    COMPATIBLE = auto()
    MAYBE_COMPATIBLE = auto()
    NOT_COMPATIBLE = auto()


def check_protocol_compatibility(version: Version) -> ProtocolCompatibility:
    """
    Checks if the given protocol version is compatible with the current one.

    Args:
        version - The protocol version to check.
    """
    if version.major != API_PROTOCOL_VERSION.major:
        return ProtocolCompatibility.NOT_COMPATIBLE
    elif version.minor != API_PROTOCOL_VERSION.minor:
        return ProtocolCompatibility.MAYBE_COMPATIBLE

    return ProtocolCompatibility.COMPATIBLE
