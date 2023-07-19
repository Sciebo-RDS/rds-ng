from typing import Protocol


class LoggerProtocol(Protocol):
    """
    Defines the general interface for our extended ``Logger``.
    """
    def debug(self, msg: str, *, scope: str | None = None, **kwargs) -> None: ...
    def info(self, msg: str, *, scope: str | None = None, **kwargs) -> None: ...
    def warning(self, msg: str, *, scope: str | None = None, **kwargs) -> None: ...
    def error(self, msg: str, *, scope: str | None = None, **kwargs) -> None: ...
