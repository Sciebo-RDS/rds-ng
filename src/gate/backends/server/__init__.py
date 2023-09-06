from .server_backend_service import create_server_backend_service
from .. import BackendsCatalog

BackendsCatalog.register_item("server", create_server_backend_service)
