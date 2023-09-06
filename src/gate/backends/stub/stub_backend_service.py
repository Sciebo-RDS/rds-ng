from common.py.component import BackendComponent
from common.py.services import Service


def create_stub_backend_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from .stub_backend_service_context import StubBackendServiceContext

    svc = comp.create_service(
        "Stub Backend service", context_type=StubBackendServiceContext
    )

    return svc
