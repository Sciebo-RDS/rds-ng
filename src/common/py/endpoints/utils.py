import http

from flask import abort, jsonify, make_response, request


def abort_request(
    message: str, *, error: str = "", code: int = http.HTTPStatus.BAD_REQUEST
) -> None:
    """
    Aborts a Flask request with a specific message and status code.

    Args:
        message: The message to be displayed to the user.
        error: The error message.
        code: The HTTP status code.
    """

    abort(
        make_response(
            jsonify(message=message, error=error if error != "" else message), code
        )
    )


def verify_request_api_header() -> None:
    """
    Verifies that the API header is valid.
    """
    from ..component import BackendComponent
    from ..settings import NetworkSettingIDs

    api_key_header = "X-RDS-NG-API-Key"

    comp = BackendComponent.instance()

    if api_key_header not in request.headers:
        abort_request("API key header missing")
    api_key = request.headers[api_key_header]
    if api_key != comp.data.config.value(NetworkSettingIDs.API_KEY):
        abort_request(message="API key mismatch")
