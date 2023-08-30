import dataclasses

from .version import API_PROTOCOL_VERSION
from ..core.messaging import Event, Message
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
