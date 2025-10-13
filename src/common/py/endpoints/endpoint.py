import dataclasses

import flask.typing


@dataclasses.dataclass(kw_only=True, frozen=True)
class Endpoint:
    """
    Defines a simple Flask endpoint.
    """

    name: str
    path: str

    handler: flask.typing.RouteCallable
