from sqlalchemy import Table, MetaData, Column, Text, String, Float, Integer
from sqlalchemy.orm import registry, composite

from common.py.data.entities.connector import Connector

from .types import JSONEncodedDataType


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

    table_connectors = Table(
        "connectors",
        metadata,
        # Main
        Column("connector_id", String(64), primary_key=True),
        Column("category", Text),
        Column("name", Text),
        Column("description", Text),
        Column("options", Integer),
        # Logos
        Column("logos__default", Text),
        Column("logos__horizontal", Text),
        # Metadata
        Column("metadata_profile", JSONEncodedDataType),
        # Miscellaneous
        Column("announce_timestamp", Float),
    )

    reg.map_imperatively(
        Connector,
        table_connectors,
        properties={
            "logos": composite(
                Connector.Logos,
                table_connectors.c.logos__default,
                table_connectors.c.logos__horizontal,
            ),
        },
    )

    return table_connectors
