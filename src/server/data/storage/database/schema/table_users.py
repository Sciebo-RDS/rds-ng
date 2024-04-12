from sqlalchemy import MetaData, Table, Column
from sqlalchemy.orm import registry

from common.py.data.entities.user import User

from .types import DataclassDataType


def register_users_table(metadata: MetaData, reg: registry) -> Table:
    """
    Registers the users table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created table.
    """
    from sqlalchemy import Unicode

    table_users = Table(
        "users",
        metadata,
        # Main
        Column("user_id", Unicode, primary_key=True),
        # Settings
        Column(
            "user_settings",
            DataclassDataType[User.Settings](dataclass_type=User.Settings),
        ),
    )

    reg.map_imperatively(User, table_users)

    return table_users
