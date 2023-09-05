from .stub_backend_service import create_stub_backend_service
from .. import BackendsCatalog

BackendsCatalog.register_item("stub", create_stub_backend_service)
