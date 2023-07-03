import typing

from .message import MessageName, MessageType


class MessageTypesCatalog:
    _message_types: typing.Dict[MessageName, type[MessageType]] = {}

    @staticmethod
    def register_type(name: MessageName, msg_type: type[MessageType]) -> None:
        if name in MessageTypesCatalog._message_types:
            if MessageTypesCatalog._message_types[name] != msg_type:
                raise RuntimeError(f"A message with the name '{name}' has already been registered to a different message type")
        else:
            MessageTypesCatalog._message_types[name] = msg_type
    
    @staticmethod
    def find_type(name: MessageName) -> type[MessageType] | None:
        return MessageTypesCatalog._message_types[name] if name in MessageTypesCatalog._message_types else None
