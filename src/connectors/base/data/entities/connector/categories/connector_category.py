from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ConnectorCategory:
    """
    Description of a connector category.

    Attributes:
        name: The category name.
    """

    name: str
