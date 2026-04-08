from flask import abort, request

from common.py.settings import NetworkSettingIDs

from ..component import ServerComponent

api_key_header = "X-RDS-NG-API-Key"


def verify_request_api_header() -> None:
    comp = ServerComponent.instance()

    if api_key_header not in request.headers:
        abort(400, {"message": "API key header missing"})
    api_key = request.headers[api_key_header]
    if api_key != comp.data.config.value(NetworkSettingIDs.API_KEY):
        abort(400, {"message": "API key mismatch"})
