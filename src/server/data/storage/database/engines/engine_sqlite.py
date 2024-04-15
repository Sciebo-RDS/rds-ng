from .engine import EngineParameters


def get_engine_parameters_sqlite(filename: str) -> EngineParameters:
    from sqlalchemy import StaticPool

    if filename == "":
        filename = "/:memory:"

    db_url = f"sqlite:///{filename}"
    connect_args = {"check_same_thread": False}
    engine_args = {"poolclass": StaticPool}

    return db_url, connect_args, engine_args
