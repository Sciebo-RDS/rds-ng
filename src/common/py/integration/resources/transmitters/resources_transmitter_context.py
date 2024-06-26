from dataclasses import dataclass

from common.py.data.entities.resource import ResourcesList


@dataclass(kw_only=True)
class ResourcesTransmitterContext:
    """
    Internal data stored by the `ResourcesTransmitter`.

    Attributes:
        resources: List of all available resources.
    """

    resources: ResourcesList | None = None
