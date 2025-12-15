from .tenant_configurations import TenantPublicConfiguration, TenantPrivateConfiguration


class Tenant:
    """
    A single tenant with its configuration.
    """

    def __init__(
        self,
        tenant_id: str,
        *,
        public_config: TenantPublicConfiguration,
        private_config: TenantPrivateConfiguration
    ):
        self._tenant_id = tenant_id

        self._public_config = public_config
        self._private_config = private_config

    @property
    def tenant_id(self) -> str:
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
