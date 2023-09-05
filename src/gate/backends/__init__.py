from .backend import mount_backend
from .backends_catalog import BackendsCatalog

# Import all backend drivers to automatically add them to the catalog
from .server import *
from .legacy import *
from .stub import *
