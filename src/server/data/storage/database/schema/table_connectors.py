from sqlalchemy import Table, MetaData, Column, Text
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

    table = Table(
        "connectors",
        metadata,
        Column("connector_id", Unicode, primary_key=True),
        Column("name", Unicode),
        Column("description", Unicode),
        Column("logo_default", Text),
        Column("logo_horizontal", Text),
        Column("metadata_profile", JSONEncodedDataType),
    )

    reg.map_imperatively(
        Connector,
        table,
        properties={
            "logos": composite(
                Connector.Logos,
                table.c.logo_default,
                table.c.logo_horizontal,
            ),
        },
    )

    return table
