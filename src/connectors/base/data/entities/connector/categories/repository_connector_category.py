import typing
from dataclasses import dataclass

from common.py.data.entities.connector import ConnectorCategoryID

from .connector_category import ConnectorCategory


@dataclass(frozen=True, kw_only=True)
class RepositoryConnectorCategory(ConnectorCategory):
    category_id: typing.ClassVar[ConnectorCategoryID] = "repository"

    def __init__(self):
        super().__init__(name="Repository")
