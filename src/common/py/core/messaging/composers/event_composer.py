from .message_composer import MessageComposer
from ..meta import MessageMetaInformation


class EventComposer(MessageComposer):
    """
    Composer for ``Event`` messages.
    """

    def _create_meta_information(
        self, suppress_logging: bool
    ) -> MessageMetaInformation:
        from ..meta import EventMetaInformation

        return EventMetaInformation(
            entrypoint=MessageMetaInformation.Entrypoint.LOCAL,
            suppress_logging=suppress_logging,
        )
