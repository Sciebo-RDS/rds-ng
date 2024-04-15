from common.py.utils.config import SettingID


class StorageSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general storage settings.

    Attributes:
        DRIVER: The driver to use for the storage; possible values are *memory* or *database* (value type: ``string``).
        DEFAULT_ROOT_PATH: The default root path for resources traversal.
    """
    DRIVER = SettingID("storage", "driver")

    DEFAULT_ROOT_PATH = SettingID("storage", "default_root_path")


class DatabaseStorageSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for database storage settings.

    Attributes:
        ENGINE: The database backend to use; can be *sqlite*, *postgresql*, *mysql* or *mariadb* (value type: ``string``).
        DUMP_SQL: If enabled, SQL statements executed will be echoed (value type: ``bool``).
    """

    ENGINE = SettingID("storage.database", "engine")
    DUMP_SQL = SettingID("storage.database", "dump_sql")

    class SQLite:
        """
        SQLite specific settings.

        Attributes:
            FILE: The (absolute) filename; if not set, an in-memory database will be used.
        """

        FILE = SettingID("storage.database.sqlite", "file")

    class PostgreSQL:
        """
        PostgreSQL specific settings.

        Attributes:
            HOST: The host of the database.
            PORT: The port of the database; if omitted, the default port will be used.
            DATABASE: The name of the database to use.
            USER: The database username.
            PASSWORD: The password for the database user.
        """

        HOST = SettingID("storage.database.postgresql", "host")
        PORT = SettingID("storage.database.postgresql", "port")
        DATABASE = SettingID("storage.database.postgresql", "database")
        USER = SettingID("storage.database.postgresql", "user")
        PASSWORD = SettingID("storage.database.postgresql", "password")

    class MySQL:
        """
        MySQL specific settings.

        Attributes:
            HOST: The host of the database.
            PORT: The port of the database; if omitted, the default port will be used.
            DATABASE: The name of the database to use.
            USER: The database username.
            PASSWORD: The password for the database user.
        """

        HOST = SettingID("storage.database.mysql", "host")
        PORT = SettingID("storage.database.mysql", "port")
        DATABASE = SettingID("storage.database.mysql", "database")
        USER = SettingID("storage.database.mysql", "user")
        PASSWORD = SettingID("storage.database.mysql", "password")

    class MariaDB:
        """
        MariaDB specific settings.

        Attributes:
            HOST: The host of the database.
            PORT: The port of the database; if omitted, the default port will be used.
            DATABASE: The name of the database to use.
            USER: The database username.
            PASSWORD: The password for the database user.
        """

        HOST = SettingID("storage.database.mariadb", "host")
        PORT = SettingID("storage.database.mariadb", "port")
        DATABASE = SettingID("storage.database.mariadb", "database")
        USER = SettingID("storage.database.mariadb", "user")
        PASSWORD = SettingID("storage.database.mariadb", "password")
