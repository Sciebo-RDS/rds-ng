from sqlalchemy import Table, MetaData, Column, TypeDecorator, Unicode
from sqlalchemy.orm import registry

from common.py.data.entities.connector import Connector

from .types import JSONEncodedDataType


class ConnectorLogosType(TypeDecorator):
    """
    Database type for connector logos.
    """

    impl = Unicode

    cache_ok = True

    def process_bind_param(self, value: Connector.Logos, dialect) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(
        self, value: str | None, dialect
    ) -> Connector.Logos | None:
        return Connector.Logos.schema().loads(value) if value is not None else None


def register_connectors_table(metadata: MetaData, reg: registry) -> Table:
    """
    Registers the connectors table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created table.
    """
    from sqlalchemy import Unicode

    table = Table(
        "connectors",
        metadata,
        Column("connector_id", Unicode, primary_key=True),
        Column("name", Unicode),
        Column("description", Unicode),
        Column("logos", ConnectorLogosType),
        Column("metadata_profile", JSONEncodedDataType),
    )

    from common.py.data.entities.connector import Connector

    reg.map_imperatively(Connector, table)

    return table
