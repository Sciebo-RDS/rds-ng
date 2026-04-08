import dataclasses
import typing

import flask.typing


@dataclasses.dataclass(kw_only=True, frozen=True)
class Endpoint:
    """
    Defines a simple Flask endpoint.

    Attributes
        name: Name of the endpoint.
        path: Path to the endpoint.
        methods: List of HTTP methods.
        handler: Handler for the endpoint.
    """

    name: str
    path: str

    methods: typing.List[str] = dataclasses.field(default_factory=lambda: ["GET"])

    handler: flask.typing.RouteCallable
