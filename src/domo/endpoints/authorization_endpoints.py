import http
import typing

import flask

from common.py.endpoints import Endpoint


def authorization_redirect_ep() -> Endpoint:
    def _handler(strategy: str) -> typing.Any:
        from ..integration.authorization import get_issuer_url

        try:
            issuer_url = get_issuer_url(strategy)
            return flask.redirect(issuer_url, code=http.HTTPStatus.SEE_OTHER)
        except Exception as e:
            return (
                {
                    "message": f"Invalid authorization information for strategy {strategy}",
                    "error": str(e),
                },
                http.HTTPStatus.BAD_REQUEST,
            )

    return Endpoint(
        name="authorization_redirect", path="/authorize/<strategy>", handler=_handler
    )
