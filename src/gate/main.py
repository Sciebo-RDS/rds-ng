from common.py.component import BackendComponent


def run_gate(comp: BackendComponent) -> None:
    """
    Runs the gate component.

    Args:
        comp: The main component instance.
    """
    from .backends import mount_backend
    from .settings import BackendSettingIDs

    try:
        mount_backend(comp.data.config.value(BackendSettingIDs.DRIVER), comp)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        from common.py.core.logging import error

        error(
            f"Unable to mount the backend: {str(exc)}",
            driver=comp.data.config.value(BackendSettingIDs.DRIVER),
        )
        exit(-1)
