from sqlalchemy import MetaData, Table, Column, TypeDecorator, Unicode
from sqlalchemy.orm import registry

from common.py.data.entities.user import User, UserSettings


class UserSettingsType(TypeDecorator):
    """
    Database type for user settings.
    """

    impl = Unicode

    cache_ok = True

    def process_bind_param(self, value: UserSettings, dialect) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(self, value: str | None, dialect) -> UserSettings | None:
        return UserSettings.schema().loads(value) if value is not None else None


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

    table = Table(
        "users",
        metadata,
        # Main
        Column("user_id", Unicode, primary_key=True),
        # Settings
        Column("user_settings", UserSettingsType),
    )

    reg.map_imperatively(User, table)

    return table
