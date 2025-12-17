import typing

from common.py.core import logging
from common.py.utils.config import Configuration

from .tenant import create_tenant_from_configuration, Tenant, TenantID


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
        self._config = Configuration(env_prefix="RDS_TENANT")
        self._config.load(config_file)

        self._tenants = self._create_tenants()

    def get_tenant(self, tenant_id: TenantID) -> Tenant | None:
        """
        Gets the tenant with the given ID or None if not found.

        Args:
            tenant_id: The tenant ID to retrieve.

        Returns:
            The tenant with the given ID.
        """
        return self._tenants[tenant_id] if tenant_id in self._tenants else None

    def _create_tenants(self) -> typing.Dict[TenantID, Tenant]:
        logging.debug(
            f"Loading tenants", config_file=self._config.settings_file, scope="tenants"
        )

        tenants = self._parse_tenants()

        logging.info(
            f"Registered tenants: {'; '.join(tenants.keys())}", scope="tenants"
        )

        return tenants

    def _parse_tenants(self) -> typing.Dict[TenantID, Tenant]:
        tenants: typing.Dict[TenantID, Tenant] = {}

        root_entries = self._config.settings.keys()
        for tenant_id in root_entries:
            tenant = create_tenant_from_configuration(self._config, tenant_id=tenant_id)
            tenants[tenant_id] = tenant

        return tenants

    @property
    def tenants(self) -> typing.Dict[TenantID, Tenant]:
        """
        All loaded tenants.
        """
        return self._tenants
