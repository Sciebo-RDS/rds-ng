import typing

from .message import Message
from .message_payload import Payload
from ...utils import UnitID


def unpack_message(
    msg_name: str, data: str, *, comp_id: UnitID, payload: Payload | None = None
) -> Message:
    """
    Unpacks a message from string data.

    Args:
        msg_name: The name of the message.
        data: The data as a JSON string.
        comp_id: The identifier of the receiving component.
        payload: An optional payload.

    Returns:
        The unpacked message.
    """

    # Look up the actual message via its name
    from .message_types_catalog import MessageTypesCatalog

    msg_type = MessageTypesCatalog.find_item(msg_name)
    if msg_type is None:
        raise RuntimeError(f"The message type '{msg_name}' is unknown")

    # Unpack the message into its actual type
    msg = typing.cast(Message, msg_type.schema().loads(data))
    msg.hops.append(comp_id)
    if payload is not None:
        msg.payload.decode(payload)

    return msg
