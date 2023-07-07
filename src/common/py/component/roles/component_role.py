import abc
import dataclasses


class ComponentRole(abc.ABC):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class NetworkingAspects:
        has_server: bool
        has_client: bool
        
    def __init__(self, role_name: str, *, networking_aspects: NetworkingAspects):
        self._name = role_name
        
        self._networking_aspects = networking_aspects
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def networking_aspects(self) -> NetworkingAspects:
        return self._networking_aspects
