import typing

from common.py.core import logging
from common.py.utils.config import Configuration

from .tenant import Tenant
from .tenant_configurations import TenantPrivateConfiguration, TenantPublicConfiguration


class Tenants:
    """
    Manages tenants and their individual configurations.
    """

    def __init__(
        self,
        *,
        config_file: str = "./.config/tenants.toml",
    ):
        """
        Args:
            config_file: The configuration file to load.
        """
        self._tenants: typing.Dict[str, Tenant] = self._load_tenants(config_file)

    def _load_tenants(self, config_file: str) -> typing.Dict[str, Tenant]:
        logging.debug(f"Loading tenants", config_file=config_file, scope="tenants")

        config = Configuration()
        config.load(config_file)

        tenants = self._parse_tenants(config)

        logging.info(
            f"Registered tenants: {'; '.join(tenants.keys())}", scope="tenants"
        )

        return tenants

    def _parse_tenants(self, config: Configuration) -> typing.Dict[str, Tenant]:
        tenants: typing.Dict[str, Tenant] = {}

        root_entries = config.settings.keys()
        for tenant_id in root_entries:
            tenant = self._create_tenant(tenant_id, config)
            tenants[tenant_id] = tenant

        return tenants

    def _create_tenant(self, tenant_id: str, config: Configuration) -> Tenant:
        # TODO
        public_config = TenantPublicConfiguration(host_url="", host_scheme="oauth2")
        private_config = TenantPrivateConfiguration()

        return Tenant(
            tenant_id, public_config=public_config, private_config=private_config
        )

    @property
    def tenants(self) -> typing.Dict[str, Tenant]:
        """
        All loaded tenants.
        """
        return self._tenants
