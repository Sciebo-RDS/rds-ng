import json
import typing
import urllib.parse
from base64 import b64decode

import flask

from common.py.integration.authorization import AuthorizationRequestPayload


def get_issuer_url(strategy: str) -> str:
    # New strategies must be added here

    def _oauth2_issuer_url() -> str:
        if "state" not in flask.request.args:
            raise RuntimeError("Missing state parameter")

        state = flask.request.args["state"]
        payload = b64decode(state).decode()
        payload_data = typing.cast(AuthorizationRequestPayload, json.loads(payload))

        issuer_url = urllib.parse.urlsplit(payload_data["auth_issuer_url"])
        issuer_url = issuer_url._replace(query=flask.request.query_string.decode())
        return str(urllib.parse.urlunsplit(issuer_url))

    if strategy.lower() == "oauth2":
        return _oauth2_issuer_url()

    raise RuntimeError("Unsupported authorization strategy")
