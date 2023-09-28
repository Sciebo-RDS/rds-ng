from .message_dispatcher import MessageDispatcher
from ..event import Event
from ..meta import EventMetaInformation


class EventDispatcher(MessageDispatcher[Event]):
    # pylint: disable=protected-access
    """
    Message dispatcher specific to ``Event``.
    """

    def __init__(self):
        super().__init__(EventMetaInformation)

    def pre_dispatch(self, msg: Event, msg_meta: EventMetaInformation) -> None:
        """
        Adds command meta information to a global list so that command replies can be handled properly.

        Args:
            msg: The command that is about to be dispatched.
            msg_meta: The command meta information.
        """
        from ...logging import debug

        debug(f"Dispatching event: {msg}", scope="bus")
        super().pre_dispatch(msg, msg_meta)
