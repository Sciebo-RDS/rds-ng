from dataclasses import dataclass

ConnectorCategoryID = str


@dataclass(frozen=True, kw_only=True)
class ConnectorCategory:
    """
    Descriptor for a connector category.

    Attributes:
        name: The category name.
        description: An optional description.
    """

    name: str
    description: str
