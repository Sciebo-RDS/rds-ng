import typing

from flask import request

from common.py.core.messaging import Channel
from common.py.endpoints.endpoint import Endpoint

from ..component import ServerComponent


def api_v1_ep() -> Endpoint:
    # The main API POST endpoint (/api/v1) accepts and processes messages in plain JSON format
    def _handler() -> typing.Any:
        from .utils import verify_request_api_header, abort_request

        # Using this EP always requires a valid API key passed via header, even if the message itself isn't protected
        verify_request_api_header()

        request_data = request.get_json(silent=True)

        if request_data is not None:
            comp = ServerComponent.instance()

            # Always target the server to prevent unintended routing
            request_data["target"] = str(Channel.direct(comp.data.comp_id))
        else:
            abort_request("Invalid data provided")

        return {"nanu": request_data}

    return Endpoint(name="api_v1", path="/api/v1", handler=_handler, methods=["POST"])
