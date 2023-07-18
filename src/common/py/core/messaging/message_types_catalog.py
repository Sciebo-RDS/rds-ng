import typing

from .message import MessageName, MessageType


class MessageTypesCatalog:
    """
    Global catalog of all registered message types.
    
    This is a globally accessible list of all message types, associated with their respective message names.
    It's mainly used to create proper message objects from incoming network messages.
    """
    _message_types: typing.Dict[MessageName, type[MessageType]] = {}

    @staticmethod
    def register_type(name: MessageName, msg_type: type[MessageType]) -> None:
        """
        Registers a new message type.
        
        Args:
            name: The message name.
            msg_type: The message type.
        """
        if name in MessageTypesCatalog._message_types:
            if MessageTypesCatalog._message_types[name] != msg_type:
                raise RuntimeError(f"A message with the name '{name}' has already been registered to a different message type")
        else:
            MessageTypesCatalog._message_types[name] = msg_type
    
    @staticmethod
    def find_type(name: MessageName) -> type[MessageType] | None:
        """
        Finds the message type associated with the given `name`.
        
        Args:
            name: The message name.

        Returns:
            The associated message type, if any.
        """
        return MessageTypesCatalog._message_types[name] if name in MessageTypesCatalog._message_types else None
