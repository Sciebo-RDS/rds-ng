from flask import Flask

from .endpoint import Endpoint


def register_endpoint(flask: Flask, ep: Endpoint) -> None:
    """
    Register an HTTP endpoint.

    Args:
        flask: The flask instance.
        ep: The endpoint to register.
    """
    flask.add_url_rule(ep.path, ep.name, view_func=ep.handler, methods=ep.methods)
