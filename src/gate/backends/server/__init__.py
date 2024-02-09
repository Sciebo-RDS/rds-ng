from .server_backend import ServerBackend
from .. import BackendsCatalog

BackendsCatalog.register_item("server", ServerBackend)
