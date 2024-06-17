import typing

from common.py.utils.config import SettingID


def get_server_settings() -> typing.Dict[SettingID, typing.Any]:
    """
    Gets default values for all server settings.

    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """
    from .storage_setting_ids import StorageSettingIDs, DatabaseStorageSettingIDs

    return {
        # Storage
        StorageSettingIDs.DRIVER: "memory",
        # Database storage
        DatabaseStorageSettingIDs.ENGINE: "sqlite",
        DatabaseStorageSettingIDs.DUMP_SQL: False,
        # Database storage: SQLite
        DatabaseStorageSettingIDs.SQLite.FILE: ":memory:",
        # Database storage: PostgreSQL
        DatabaseStorageSettingIDs.PostgreSQL.HOST: "",
        DatabaseStorageSettingIDs.PostgreSQL.PORT: 0,
        DatabaseStorageSettingIDs.PostgreSQL.DATABASE: "rds_ng",
        DatabaseStorageSettingIDs.PostgreSQL.USER: "",
        DatabaseStorageSettingIDs.PostgreSQL.PASSWORD: "",
        # Database storage: MySQL
        DatabaseStorageSettingIDs.MySQL.HOST: "",
        DatabaseStorageSettingIDs.MySQL.PORT: 0,
        DatabaseStorageSettingIDs.MySQL.DATABASE: "rds_ng",
        DatabaseStorageSettingIDs.MySQL.USER: "",
        DatabaseStorageSettingIDs.MySQL.PASSWORD: "",
        # Database storage: MariaDB
        DatabaseStorageSettingIDs.MariaDB.HOST: "",
        DatabaseStorageSettingIDs.MariaDB.PORT: 0,
        DatabaseStorageSettingIDs.MariaDB.DATABASE: "rds_ng",
        DatabaseStorageSettingIDs.MariaDB.USER: "",
        DatabaseStorageSettingIDs.MariaDB.PASSWORD: "",
    }
