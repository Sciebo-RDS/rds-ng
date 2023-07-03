import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkingAspects:
    has_server: bool
    has_client: bool
