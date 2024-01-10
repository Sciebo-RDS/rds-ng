from common.py.component import BackendComponent
from common.py.services import Service


def create_stub_connectors_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend connectors service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from gate.backends.stub.stub_service_context import StubServiceContext

    svc = comp.create_service("Connectors service", context_type=StubServiceContext)

    return svc
