from common.py.component import BackendComponent
from common.py.services import Service


def mount_backend(driver: str, comp: BackendComponent) -> Service:
    """
    Mounts the configured backend.

    Args:
        driver: The backend driver to use.
        comp: The main component instance.

    Returns:
        The newly created backend service.

    Raises:
        RuntimeError: If the specified driver couldn't be found.
    """
    from .backends_catalog import BackendsCatalog

    creator = BackendsCatalog.find_item(driver)
    if creator is None:
        raise RuntimeError(f"The backend driver {driver} couldn't be found")

    return creator(comp)
