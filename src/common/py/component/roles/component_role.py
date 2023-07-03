import abc

from .aspects import MessagingAspects, NetworkingAspects


class ComponentRole(abc.ABC):
    def __init__(self, role_name: str, *, messaging_aspects: MessagingAspects, networking_aspects: NetworkingAspects):
        self._name = role_name
        
        self._messaging_aspects = messaging_aspects
        self._networking_aspects = networking_aspects
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def messaging_aspects(self) -> MessagingAspects:
        return self._messaging_aspects
    
    @property
    def networking_aspects(self) -> NetworkingAspects:
        return self._networking_aspects
