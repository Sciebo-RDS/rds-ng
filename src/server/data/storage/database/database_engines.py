from sqlalchemy import Engine, create_engine

from common.py.core.logging import debug
from common.py.utils.config import Configuration


def _create_db_url(
    host: str, port: int, database: str, user: str, password: str
) -> str:
    if user == "" or password == "":
        raise RuntimeError("No user credentials provided")
    if database == "":
        raise RuntimeError("No database name provided")

    url = f"{user}:{password}@{host}"
    if port != 0:
        url += f":{port}"
    url += f"/{database}"
    return url


def create_database_engine(config: Configuration) -> Engine:
    from ....settings.storage_setting_ids import DatabaseStorageSettingIDs

    engine = config.value(DatabaseStorageSettingIDs.ENGINE)

    connect_args = {}
    engine_args = {}
    dump_sql = config.value(DatabaseStorageSettingIDs.DUMP_SQL)

    if engine == "sqlite":
        from sqlalchemy import StaticPool

        db_url = f"sqlite://{config.value(DatabaseStorageSettingIDs.SQLite.FILE)}"
        connect_args = {"check_same_thread": False}
        engine_args = {"poolclass": StaticPool}
    elif engine == "postgresql":
        db_url = "postgresql://" + _create_db_url(
            config.value(DatabaseStorageSettingIDs.PostgreSQL.HOST),
            config.value(DatabaseStorageSettingIDs.PostgreSQL.PORT),
            config.value(DatabaseStorageSettingIDs.PostgreSQL.DATABASE),
            config.value(DatabaseStorageSettingIDs.PostgreSQL.USER),
            config.value(DatabaseStorageSettingIDs.PostgreSQL.PASSWORD),
        )
    elif engine == "mysql":
        db_url = "mysql://" + _create_db_url(
            config.value(DatabaseStorageSettingIDs.MySQL.HOST),
            config.value(DatabaseStorageSettingIDs.MySQL.PORT),
            config.value(DatabaseStorageSettingIDs.MySQL.DATABASE),
            config.value(DatabaseStorageSettingIDs.MySQL.USER),
            config.value(DatabaseStorageSettingIDs.MySQL.PASSWORD),
        )
    elif engine == "mariadb":
        db_url = "mariadb://" + _create_db_url(
            config.value(DatabaseStorageSettingIDs.MariaDB.HOST),
            config.value(DatabaseStorageSettingIDs.MariaDB.PORT),
            config.value(DatabaseStorageSettingIDs.MariaDB.DATABASE),
            config.value(DatabaseStorageSettingIDs.MariaDB.USER),
            config.value(DatabaseStorageSettingIDs.MariaDB.PASSWORD),
        )
    else:
        raise RuntimeError(f"Unknown database engine '{engine}'")

    if db_url == "":
        raise RuntimeError("No database URL was generated")

    debug("Creating database engine", scope="database", engine=engine, url=db_url)

    return create_engine(
        db_url,
        echo=dump_sql,
        connect_args=connect_args,
        **engine_args,
    )
