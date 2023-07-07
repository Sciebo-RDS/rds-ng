import typing

from .. import Message, MessageType, Command, CommandReply, Event
from ..meta import MessageMetaInformation, MessageMetaInformationType, CommandMetaInformation, CommandReplyMetaInformation, EventMetaInformation


class MessageMetaInformationCreator:
    _meta_information_types: typing.Dict[type[MessageType], type[MessageMetaInformationType]] = {
        Command: CommandMetaInformation,
        CommandReply: CommandReplyMetaInformation,
        Event: EventMetaInformation,
    }
    
    @staticmethod
    def create_meta_information(msg: Message, entrypoint: MessageMetaInformation.Entrypoint, **kwargs) -> MessageMetaInformationType:
        for msg_type, meta_type in MessageMetaInformationCreator._meta_information_types.items():
            if isinstance(msg, msg_type):
                return meta_type(entrypoint=entrypoint, **kwargs)
        else:
            raise RuntimeError("No meta information type associated with message type")
