from common.py.component import BackendComponent
from common.py.services import Service


def create_legacy_backend_service(comp: BackendComponent) -> Service:
    """
    Creates the legacy backend service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from .legacy_backend_service_context import LegacyBackendServiceContext

    svc = comp.create_service(
        "Legacy Backend service", context_type=LegacyBackendServiceContext
    )

    return svc
