import typing

from flask import abort, request

from common.py.endpoints.endpoint import Endpoint


def api_v1_ep() -> Endpoint:
    # The main API POST endpoint (/api/v1) accepts and processes messages in plain JSON format
    def _handler() -> typing.Any:
        from .utils import verify_request_api_header

        # Using this EP always requires a valid API key passed via header, even if the message itself isn't protected
        verify_request_api_header()

        request_data = request.get_json()
        return {"nanu": request_data}

    return Endpoint(name="api_v1", path="/api/v1", handler=_handler, methods=["POST"])
