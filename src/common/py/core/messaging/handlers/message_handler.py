import typing

from ..message import MessageType


MessageHandler = typing.Callable[[typing.Generic[MessageType]], None]  # TODO: Subject to change (UoW, etc.)
