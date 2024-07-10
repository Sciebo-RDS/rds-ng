import typing
from dataclasses import dataclass, field

from common.py.data.entities.resource import Resource


@dataclass(kw_only=True)
class ConnectorJobTransmissionContext:
    """
    A helper context to manage file transmissions.

    Attributes:
        resources: The list of resources to transmit.
        current_index: The resource currently being processed.
    """

    resources: typing.List[Resource]

    current_index: int

    @property
    def current_resource(self) -> Resource:
        return self.resources[self.current_index]

    @property
    def is_done(self) -> bool:
        return self.current_index >= len(self.resources)
