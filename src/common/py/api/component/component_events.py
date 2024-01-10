import dataclasses

from ..version import API_PROTOCOL_VERSION
from ...core.messaging import Event, Message
from ...core.messaging.composers import MessageBuilder, EventComposer
from ...utils import UnitID


@dataclasses.dataclass(frozen=True, kw_only=True)
class ComponentInformation:
    """
    Component information as an object.
    """

    comp_id: UnitID
    comp_name: str
    comp_version: str


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

    comp_id: UnitID = dataclasses.field(default_factory=lambda: UnitID("", ""))

    comp_name: str = ""
    comp_version: str = ""

    api_protocol: str = str(API_PROTOCOL_VERSION)

    def component_information(self) -> ComponentInformation:
        """
        The component information bundled as an object.

        Returns:
            The component information stored in a ``ComponentInformation`` object.
        """
        return ComponentInformation(
            comp_id=self.comp_id,
            comp_name=self.comp_name,
            comp_version=self.comp_version,
        )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        comp_id: UnitID,
        comp_name: str,
        comp_version: str,
        chain: Message | None = None,
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ComponentInformationEvent,
            chain,
            comp_id=comp_id,
            comp_name=comp_name,
            comp_version=comp_version,
        )
