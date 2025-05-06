from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import database_exists, create_database

from common.py.core.logging import debug
from common.py.utils.config import Configuration


def create_database_engine(config: Configuration) -> Engine:
    from .....settings.storage_setting_ids import DatabaseStorageSettingIDs

    engine = config.value(DatabaseStorageSettingIDs.ENGINE)
    match engine:
        case "sqlite":
            from .engine_sqlite import get_engine_parameters_sqlite

            db_url, connect_args, engine_args = get_engine_parameters_sqlite(
                config.value(DatabaseStorageSettingIDs.SQLite.FILE)
            )
        case "postgresql":
            from .engine_postgresql import get_engine_parameters_postgresql

            db_url, connect_args, engine_args = get_engine_parameters_postgresql(
                config.value(DatabaseStorageSettingIDs.PostgreSQL.HOST),
                config.value(DatabaseStorageSettingIDs.PostgreSQL.PORT),
                config.value(DatabaseStorageSettingIDs.PostgreSQL.DATABASE),
                config.value(DatabaseStorageSettingIDs.PostgreSQL.USER),
                config.value(DatabaseStorageSettingIDs.PostgreSQL.PASSWORD),
            )
        case "mysql":
            from .engine_mysql import get_engine_parameters_mysql

            db_url, connect_args, engine_args = get_engine_parameters_mysql(
                config.value(DatabaseStorageSettingIDs.MySQL.HOST),
                config.value(DatabaseStorageSettingIDs.MySQL.PORT),
                config.value(DatabaseStorageSettingIDs.MySQL.DATABASE),
                config.value(DatabaseStorageSettingIDs.MySQL.USER),
                config.value(DatabaseStorageSettingIDs.MySQL.PASSWORD),
            )
        case "mariadb":
            from .engine_mariadb import get_engine_parameters_mariadb

            db_url, connect_args, engine_args = get_engine_parameters_mariadb(
                config.value(DatabaseStorageSettingIDs.MariaDB.HOST),
                config.value(DatabaseStorageSettingIDs.MariaDB.PORT),
                config.value(DatabaseStorageSettingIDs.MariaDB.DATABASE),
                config.value(DatabaseStorageSettingIDs.MariaDB.USER),
                config.value(DatabaseStorageSettingIDs.MariaDB.PASSWORD),
            )
        case _:
            raise RuntimeError(f"Unknown database engine '{engine}'")

    if db_url == "":
        raise RuntimeError("No database URL was generated")

    debug("Creating database engine", scope="database", engine=engine, url=db_url)

    if not database_exists(db_url):
        create_database(db_url)

    return create_engine(
        db_url,
        echo=config.value(DatabaseStorageSettingIDs.DUMP_SQL),
        connect_args=connect_args,
        **engine_args,
    )
