import abc
import dataclasses


class ComponentRole(abc.ABC):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class NetworkingAspect:
        has_server: bool
        has_client: bool
        
    def __init__(self, role_name: str, *, networking_aspect: NetworkingAspect):
        self._name = role_name
        
        self._networking_aspect = networking_aspect
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def networking_aspect(self) -> NetworkingAspect:
        return self._networking_aspect
