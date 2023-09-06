from .legacy_backend_service import create_legacy_backend_service
from .. import BackendsCatalog

BackendsCatalog.register_item("legacy", create_legacy_backend_service)
