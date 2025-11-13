import typing

from .endpoint import Endpoint


def info_ep() -> Endpoint:
    # The main entry point (/) returns basic component info as a JSON string
    def _handler() -> typing.Any:
        from ..component import BackendComponent

        comp = BackendComponent.instance()

        return {
            "id": str(comp.data.comp_id),
            "name": comp.data.name,
            "version": str(comp.data.version),
        }

    return Endpoint(name="info", path="/", handler=_handler)
