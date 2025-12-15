from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True, frozen=True)
class TenantPublicConfiguration:
    """
    Public tenant configuration.
    """

    host_url: str
    host_scheme: str


@dataclass_json
@dataclass(kw_only=True, frozen=True)
class TenantPrivateConfiguration:
    """
    Private tenant configuration.
    """
