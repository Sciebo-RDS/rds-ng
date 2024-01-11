from .stub_backend import StubBackend
from .. import BackendsCatalog

BackendsCatalog.register_item("stub", StubBackend)
