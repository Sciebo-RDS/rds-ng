import typing

from common.py.utils.config import Configuration

from .tenant_configurations import TenantPrivateConfiguration, TenantPublicConfiguration

TenantID = str


class Tenant:
    """
    A single tenant with its configuration.
    """

    def __init__(
        self,
        tenant_id: TenantID,
        *,
        public_config: TenantPublicConfiguration,
        private_config: TenantPrivateConfiguration,
    ):
        self._tenant_id = tenant_id

        self._public_config = public_config
        self._private_config = private_config

    @property
    def tenant_id(self) -> TenantID:
        """
        The tenant identifier.
        """
        return self._tenant_id

    @property
    def public_config(self) -> TenantPublicConfiguration:
        """
        The public tenant configuration.
        """
        return self._public_config

    @property
    def private_config(self) -> TenantPrivateConfiguration:
        """
        The private tenant configuration.
        """
        return self._private_config


def create_tenant_from_configuration(
    config: Configuration, *, tenant_id: TenantID
) -> Tenant:

    def _get_config_value(
        key: str,
        *,
        default: typing.Any | None = None,
    ) -> typing.Any:
        from common.py.utils.config import SettingID

        setting_id = SettingID(tenant_id, key)
        return config.value_with_default(setting_id, default)

    # Gather and verify public settings
    public_config = TenantPublicConfiguration(
        integration=TenantPublicConfiguration.Integration(
            scheme=_get_config_value("integration.scheme"),
            host_integration=TenantPublicConfiguration.Integration.HostIntegration(
                url=_get_config_value("integration.host.url", default=""),
                endpoints=TenantPublicConfiguration.Integration.HostIntegration.Endpoints(
                    entrypoint=_get_config_value(
                        "integration.host.endpoints.entrypoint", default=""
                    ),
                    api=_get_config_value("integration.host.endpoints.api", default=""),
                ),
            ),
        ),
        authorization=TenantPublicConfiguration.Authorization(
            oauth2=TenantPublicConfiguration.Authorization.OAuth2(
                client_id=_get_config_value(
                    "authorization.oauth2.client_id", default=""
                ),
            )
        ),
    )

    if public_config.integration.scheme == "":
        raise RuntimeError("Missing integration scheme")
    elif public_config.integration.scheme == "host":
        if public_config.integration.host_integration.url == "":
            raise RuntimeError("Missing integration host url")

    # Gather and verify private settings
    private_config = TenantPrivateConfiguration(
        authorization=TenantPrivateConfiguration.Authorization(
            oauth2=TenantPrivateConfiguration.Authorization.OAuth2(
                client_secret=_get_config_value(
                    "authorization.oauth2.client_secret", default=""
                ),
            )
        ),
        connectors=TenantPrivateConfiguration.Connectors(
            excluded_connectors=_get_config_value(
                "connectors.excluded_connectors", default=[]
            )
        ),
    )

    return Tenant(tenant_id, public_config=public_config, private_config=private_config)
