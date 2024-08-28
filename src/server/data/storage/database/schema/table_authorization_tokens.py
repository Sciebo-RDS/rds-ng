from dataclasses import dataclass

from sqlalchemy import (
    Integer,
    MetaData,
    Table,
    Column,
    Text,
    Numeric,
    String,
    ForeignKey,
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
        Column("user_id", String(256), ForeignKey("users.user_id"), primary_key=True),
        Column("auth_id", String(256), primary_key=True),
        Column("auth_type", String(32)),
        Column("auth_issuer", Text),
        Column("auth_bearer", Text),
        # Settings
        Column("state", Text),
        Column("timestamp", Numeric(32, 8, asdecimal=False)),
        Column("expiration_timestamp", Numeric(32, 8, asdecimal=False)),
        Column("refresh_attempts", Integer),
        # Data
        Column("strategy", Text),
        Column("token", JSONEncodedDataType),
        Column("data", JSONEncodedDataType),
    )

    reg.map_imperatively(
        AuthorizationToken,
        table_authorization_tokens,
    )

    return AuthorizationTokensTables(main=table_authorization_tokens)
