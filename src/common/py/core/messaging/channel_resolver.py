from enum import Flag, auto

from . import Channel
from ...component import ComponentID


class ChannelResolver:
    class TransportType(Flag):
        LOCAL = auto()
        REMOTE = auto()
    
    def __init__(self, comp_id: ComponentID):
        self._comp_id = comp_id
        
    def resolve(self, target: Channel) -> TransportType:
        transport_type = ChannelResolver.TransportType(0)
        
        if self._check_dispatch_locally(target):
            transport_type |= ChannelResolver.TransportType.LOCAL
            
        if self._check_dispatch_remotely(target):
            transport_type |= ChannelResolver.TransportType.REMOTE
        
        return transport_type

    def _check_dispatch_locally(self, target: Channel) -> bool:
        if target.is_local:
            return True
        elif target.is_direct:
            target_id = ComponentID.from_string(target.target)
            return target_id.equals(self._comp_id)
        elif target.is_room:
            # TODO: Rooms: List of subscribed rooms, check if match -> local as well (maybe remote)
            pass
        
        return False

    def _check_dispatch_remotely(self, target: Channel) -> bool:
        if target.is_local:
            return False
        elif target.is_direct:
            target_id = ComponentID.from_string(target.target)
            return not target_id.equals(self._comp_id)
        elif target.is_room:
            # TODO: Rooms: List of subscribed rooms, check if match -> local as well (maybe remote)
            pass
        
        return False
