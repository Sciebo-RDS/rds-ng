from flask import abort, jsonify, make_response, request, Response

from common.py.settings import NetworkSettingIDs

from ..component import ServerComponent


def abort_request(message: str, code: int = 400) -> None:
    """
    Aborts a Flask request with a specific message and status code.

    Args:
        message: The message to be displayed to the user.
        code: The HTTP status code.
    """

    abort(make_response(jsonify(message=message), code))


def verify_request_api_header() -> None:
    """
    Verifies that the API header is valid.
    """
    api_key_header = "X-RDS-NG-API-Key"

    comp = ServerComponent.instance()

    if api_key_header not in request.headers:
        abort_request("API key header missing")
    api_key = request.headers[api_key_header]
    if api_key != comp.data.config.value(NetworkSettingIDs.API_KEY):
        abort_request(message="API key mismatch")
