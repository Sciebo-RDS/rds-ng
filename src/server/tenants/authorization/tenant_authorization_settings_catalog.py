import typing

from common.py.data.entities.authorization import AuthorizationSettingsConfig
from common.py.utils import ItemsCatalog

from .. import Tenant

TenantAuthorizationSettingsCreator = typing.Callable[
    [
        Tenant,
    ],
    typing.Tuple[
        AuthorizationSettingsConfig | None, AuthorizationSettingsConfig | None
    ],
]


@ItemsCatalog.define()
class TenantAuthorizationSettingsCatalog(
    ItemsCatalog[TenantAuthorizationSettingsCreator]
):
    """
    Global catalog of creator functions for strategy-specific tenant authorization settings.
    """
