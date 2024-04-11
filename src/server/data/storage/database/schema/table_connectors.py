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

    table_connectors = Table(
        "connectors",
        metadata,
        # Main
        Column("connector_id", Unicode, primary_key=True),
        Column("name", Unicode),
        Column("description", Unicode),
        # Logos
        Column("logos_default", Text),
        Column("logos_horizontal", Text),
        # Metadata
        Column("metadata_profile", JSONEncodedDataType),
    )

    reg.map_imperatively(
        Connector,
        table_connectors,
        properties={
            "logos": composite(
                Connector.Logos,
                table_connectors.c.logos_default,
                table_connectors.c.logos_horizontal,
            ),
        },
    )

    return table_connectors
