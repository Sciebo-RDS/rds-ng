from dataclasses import dataclass

from sqlalchemy import MetaData, Table, Column, String, Text
from sqlalchemy.orm import registry

from common.py.data.entities.user import User

from .types import DataclassDataType


@dataclass(kw_only=True)
class UsersTables:
    main: Table


def register_users_tables(metadata: MetaData, reg: registry) -> UsersTables:
    """
    Registers the users table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created tables.
    """

    table_users = Table(
        "users",
        metadata,
        # Main
        Column("user_id", String(1024), primary_key=True),
        Column("name", Text),
        # Settings
        Column(
            "user_settings",
            DataclassDataType[User.Settings](dataclass_type=User.Settings),
        ),
    )

    reg.map_imperatively(User, table_users)

    return UsersTables(main=table_users)
