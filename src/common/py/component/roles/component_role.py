import abc

from .aspects.networking_aspects import NetworkingAspects


class ComponentRole(abc.ABC):
    def __init__(self, role_name: str, *, networking_aspects: NetworkingAspects):
        self._name = role_name
        
        self._networking_aspects = networking_aspects
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def networking_aspects(self) -> NetworkingAspects:
        return self._networking_aspects
