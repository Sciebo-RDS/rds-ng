import dataclasses

from .aspects import Aspects


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkingAspects(Aspects):
    has_server: bool
    has_client: bool
