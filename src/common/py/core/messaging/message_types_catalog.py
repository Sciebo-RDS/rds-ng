from .message import MessageType
from ...utils import ItemsCatalog


@ItemsCatalog.define()
class MessageTypesCatalog(ItemsCatalog[type[MessageType]]):
    """
    Global catalog of all registered message types.

    This is a globally accessible list of all message types, associated with their respective message names.
    It's mainly used to create proper message objects from incoming network messages.
    """
