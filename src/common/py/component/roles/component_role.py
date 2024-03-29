import abc
import dataclasses


class ComponentRole(abc.ABC):
    """
    The role definition of a component.
    
    A component role defines certain aspects of a component. This usually corresponds to having specific features
    enabled or overriding types that are used within the core.
    """
    
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class RuntimeAspects:
        """
        Runtime aspects of a role.
        
        Attributes:
            runtime_app_type: The runtime (WSGI) application type to instantiate.
        """
        runtime_app_type: type
        
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class NetworkingAspects:
        """
        Networking aspects of a role.
        
        Attributes:
            has_server: Whether this role runs a server in the networking engine.
            has_client: Whether this role runs a client in the networking engine.
        """
        has_server: bool
        has_client: bool
        
    def __init__(self, role_name: str, *, runtime_aspects: RuntimeAspects, networking_aspects: NetworkingAspects):
        """
        Args:
            role_name: The name of the role.
            networking_aspects: The networking aspects to use.
        """
        self._name = role_name
        
        self._runtime_aspects = runtime_aspects
        self._networking_aspects = networking_aspects
        
    @property
    def name(self) -> str:
        """
        The name of the role.
        """
        return self._name
    
    @property
    def runtime_aspects(self) -> RuntimeAspects:
        """
        The runtime aspects of this role.
        """
        return self._runtime_aspects
        
    @property
    def networking_aspects(self) -> NetworkingAspects:
        """
        The networking aspects of the role.
        """
        return self._networking_aspects
