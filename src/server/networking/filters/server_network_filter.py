from common.py.core.messaging import Message
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.core.messaging.networking.network_filter import NetworkFilter
from common.py.utils import UnitID


class ServerNetworkFilter(NetworkFilter):
    """
    This filter implements a few sanity checks for incoming and outgoing messages.
    """

    def __init__(self, comp_id: UnitID):
        self._comp_id = comp_id

    def filter_incoming_message(
        self,
        connection: NetworkFilter.ConnectionType,
        msg: Message,
        msg_meta: MessageMetaInformation,
    ) -> NetworkFilter.Action:
        # Only accept messages directed to this component
        if connection == NetworkFilter.ConnectionType.SERVER:
            if msg.target.is_direct and msg.target.target_id.equals(self._comp_id):
                return NetworkFilter.Action.PASS

        return NetworkFilter.Action.REJECT

    def filter_outgoing_message(
        self,
        connection: NetworkFilter.ConnectionType,
        msg: Message,
        msg_meta: MessageMetaInformation,
    ) -> NetworkFilter.Action:
        # Only allow direct messages to other components
        if connection == NetworkFilter.ConnectionType.SERVER:
            if msg.target.is_direct and not msg.target.target_id.equals(self._comp_id):
                return NetworkFilter.Action.PASS

        return NetworkFilter.Action.REJECT
