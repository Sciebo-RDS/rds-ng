import typing
from dataclasses import dataclass

from .message import Message
from .command import Command, CommandType
from .command_reply import CommandReplyCallback


@Message.define("$internal/CommandWrapper$")
class CommandWrapper(Command):
    command: CommandType | None = None

    done_callback: CommandReplyCallback | None = None
    fail_callback: CommandReplyCallback | None = None
