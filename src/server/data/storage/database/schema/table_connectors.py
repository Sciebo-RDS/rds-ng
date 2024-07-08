from dataclasses import dataclass

from sqlalchemy import Table, MetaData, Column, Text, String, Integer, Numeric
from sqlalchemy.orm import registry, composite

from common.py.data.entities.authorization import AuthorizationSettings
from common.py.data.entities.connector import Connector
from common.py.utils import UnitID

from .types import JSONEncodedDataType, DataclassDataType


@dataclass(kw_only=True)
class ConnectorsTables:
    main: Table


def register_connectors_tables(metadata: MetaData, reg: registry) -> ConnectorsTables:
    """
    Registers the connectors table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created tables.
    """
    from sqlalchemy import Unicode

    table_connectors = Table(
        "connectors",
        metadata,
        # Main
        Column("connector_id", String(64), primary_key=True),
        Column(
            "connector_address",
            DataclassDataType[UnitID](dataclass_type=UnitID),
        ),
        Column("name", Text),
        Column("description", Text),
        Column("category", Text),
        Column("options", Integer),
        # Authorization
        Column("auth__strategy", Text),
        Column("auth__config", JSONEncodedDataType),
        # Logos
        Column("logos__default", Text),
        Column("logos__horizontal", Text),
        # Metadata
        Column("metadata_profile", JSONEncodedDataType),
        # Miscellaneous
        Column("announce_timestamp", Numeric(32, 8, asdecimal=False)),
    )

    reg.map_imperatively(
        Connector,
        table_connectors,
        properties={
            "authorization": composite(
                AuthorizationSettings,
                table_connectors.c.auth__strategy,
                table_connectors.c.auth__config,
            ),
            "logos": composite(
                Connector.Logos,
                table_connectors.c.logos__default,
                table_connectors.c.logos__horizontal,
            ),
        },
    )

    return ConnectorsTables(main=table_connectors)
