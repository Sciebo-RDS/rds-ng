import typing

from flask import request

from common.py.endpoints.endpoint import Endpoint


def api_v1_ep() -> Endpoint:
    # The main API POST endpoint (/api/v1) accepts and processes messages in plain JSON format
    def _handler() -> typing.Any:
        request_data = request.get_json()
        return {"nanu": request_data}

    return Endpoint(name="api_v1", path="/api/v1", handler=_handler, methods=["POST"])
