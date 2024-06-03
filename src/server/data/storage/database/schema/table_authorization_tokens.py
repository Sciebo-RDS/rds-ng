from dataclasses import dataclass

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Text,
    Numeric,
    String,
)
from sqlalchemy.orm import registry

from common.py.data.entities.authorization import AuthorizationToken

from .types import JSONEncodedDataType


@dataclass(kw_only=True)
class AuthorizationTokensTables:
    main: Table


def register_authorization_tokens_tables(
    metadata: MetaData, reg: registry
) -> AuthorizationTokensTables:
    """
    Registers the authorization tokens table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created tables.
    """

    table_authorization_tokens = Table(
        "authorization_tokens",
        metadata,
        # Main
        Column("user_id", String(256), primary_key=True),
        Column("token_id", String(256), primary_key=True),
        # Settings
        Column("expiration_timestamp", Numeric(32, 8, asdecimal=False)),
        # Data
        Column("strategy", Text),
        Column("data", JSONEncodedDataType),
    )

    reg.map_imperatively(
        AuthorizationToken,
        table_authorization_tokens,
    )

    return AuthorizationTokensTables(main=table_authorization_tokens)
