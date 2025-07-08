import typing

from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True)
class AuthorizationStrategyConfiguration:
    """
    A set of authorization configurations, split into public and private.
    """

    public_config: typing.Dict[str, typing.Any] = field(default_factory=dict)
    private_config: typing.Dict[str, typing.Any] = field(default_factory=dict)
