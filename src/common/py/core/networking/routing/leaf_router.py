import typing

from .network_router import NetworkRouter
from ...messaging import Message
from ....component import ComponentID


class LeafRouter(NetworkRouter):
    def check_client_routing(self, msg: Message) -> bool:
        # Messages that stem from this component are always sent through the client
        return msg.origin.equals(self._comp_id)
    
    def check_server_routing(self, msg: Message) -> typing.Tuple[bool, typing.List[ComponentID]]:
        # We don't even run a server!
        return False, []
