from enum import StrEnum


class ComponentType(StrEnum):
    """
    All known component types.
    """

    INFRASTRUCTURE = "infra"
    WEB = "web"
    CONNECTOR = "connector"


class ComponentUnit(StrEnum):
    """
    All known component units.
    """

    # Infrastructure
    SERVER = "server"
    GATE = "gate"

    # Web
    FRONTEND = "frontend"
