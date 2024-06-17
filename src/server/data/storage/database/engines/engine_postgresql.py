from .engine import EngineParameters
from .engine_utils import format_database_url


def get_engine_parameters_postgresql(
    host: str, port: int, database: str, user: str, password: str
) -> EngineParameters:
    db_url = "postgresql+psycopg://" + format_database_url(
        host, port, database, user, password
    )
    return db_url, {}, {}
