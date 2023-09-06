from common.py.core.messaging import Message
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.core.messaging.networking.network_filter import NetworkFilter
from common.py.utils import UnitID


class GateFilter(NetworkFilter):
    """
    The gate only allows communication from the server and web frontends. This filter ensures that no other messages will pass.
    """

    def __init__(self, comp_id: UnitID):
        self._comp_id = comp_id

    def filter_incoming_message(
        self,
        connection: NetworkFilter.ConnectionType,
        msg: Message,
        msg_meta: MessageMetaInformation,
    ) -> bool:
        # Messages from the server side may only be directed to this component
        if connection == NetworkFilter.ConnectionType.SERVER:
            if msg.target.is_direct and not msg.target.target_id.equals(self._comp_id):
                return False

        if connection == NetworkFilter.ConnectionType.CLIENT:
            from common.py.component import ComponentType

            if msg.target.is_direct and not (
                msg.target.target_id.equals(self._comp_id)
                or msg.target.target_id.type == ComponentType.WEB
            ):
                return False

        return False

    def filter_outgoing_message(
        self,
        connection: NetworkFilter.ConnectionType,
        msg: Message,
        msg_meta: MessageMetaInformation,
    ) -> bool:
        # When a message is sent through the server connection, it may only go to a web client
        if connection == NetworkFilter.ConnectionType.SERVER:
            from common.py.component import ComponentType

            if msg.target.is_direct and msg.target.target_id.type != ComponentType.WEB:
                return True

        return False
