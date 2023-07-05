import typing

from .network_router import NetworkRouter
from ...messaging import Message
from ....component import ComponentID


class ServerRouter(NetworkRouter):
    def check_client_routing(self, msg: Message) -> bool:
        # We don't even run a client!
        return False
    
    def check_server_routing(self, msg: Message) -> typing.Tuple[bool, typing.List[ComponentID]]:
        # Messages stemming from this component go out to all clients except for self
        if msg.origin.equals(self._comp_id):
            return True, [self._comp_id]
        else:
            # TODO: Incoming
            pass
        
        # TODO: Incoming
        
        # TODO: Skip certain targets (SIDs)
        # TODO
        # Rooms und direkte Targets (!= self)
        # Origin / Hops ausschließen
        return False, []
