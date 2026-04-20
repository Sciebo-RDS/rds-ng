import http
import typing

import flask

from common.py.endpoints import abort_request, Endpoint


def authorization_redirect_ep() -> Endpoint:
    """
    Endpoint to perform an authorization redirect.

    Returns:
        The endpoint instance.
    """

    def _handler(*args, strategy: str, **kwargs) -> typing.Any:
        from ..integration.authorization import get_issuer_url

        try:
            issuer_url = get_issuer_url(strategy)
            return flask.redirect(issuer_url, code=http.HTTPStatus.SEE_OTHER)
        except Exception as e:
            abort_request(
                "Invalid authorization information for strategy {strategy}",
                error=str(e),
            )

    return Endpoint(
        name="authorization_redirect", path="/authorize/<strategy>", handler=_handler
    )
