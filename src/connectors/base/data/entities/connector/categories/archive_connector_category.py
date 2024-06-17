import typing
from dataclasses import dataclass

from common.py.data.entities.connector import ConnectorCategoryID

from .connector_category import ConnectorCategory


@dataclass(frozen=True, kw_only=True)
class ArchiveConnectorCategory(ConnectorCategory):
    category_id: typing.ClassVar[ConnectorCategoryID] = "archive"

    def __init__(self):
        super().__init__(name="Archive")
