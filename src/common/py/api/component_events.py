import dataclasses

from .version import API_PROTOCOL_VERSION
from ..core.messaging import Event, Message, Channel
from ..core.messaging.handlers import MessageEmitter
from ..utils import UnitID


@Message.define("event/component/information")
class ComponentInformationEvent(Event):
    """
    Contains information about a connected component; this is automatically sent whenever a connection is established (bilaterally).

    Attributes:
        comp_id: The component ID.
        comp_name: The component name.
        comp_version: The component version.
        api_protocol: The API protocol version.
    """

    comp_id: UnitID = dataclasses.field(default_factory=UnitID)

    comp_name: str = ""
    comp_version: str = ""

    api_protocol: int = API_PROTOCOL_VERSION

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        comp_id: UnitID,
        comp_name: str,
        comp_version: str,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_event(
            ComponentInformationEvent,
            target,
            chain=chain,
            comp_id=comp_id,
            comp_name=comp_name,
            comp_version=comp_version,
        )
