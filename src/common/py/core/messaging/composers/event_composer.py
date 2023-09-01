from .message_composer import MessageComposer
from ..meta import MessageMetaInformation


class EventComposer(MessageComposer):
    """
    Composer for ``Event`` messages.
    """

    def _create_meta_information(self) -> MessageMetaInformation:
        from ..meta import EventMetaInformation

        return EventMetaInformation(entrypoint=MessageMetaInformation.Entrypoint.LOCAL)
