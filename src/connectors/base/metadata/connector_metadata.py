from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Dict, List


@dataclass
class ConnectorMetadata(ABC):

    def __iter__(self):
        return (getattr(self, field.name) for field in fields(self))


class ConnectorMetadataFactory(ABC):

    @abstractmethod
    def create(metadata: List[Dict[str, Any]]) -> ConnectorMetadata:
        pass

    def validate(metadata: ConnectorMetadata) -> None:
        if not all(metadata):
            raise ValueError(
                f"Invalid metadata, property {[field.name for field in fields(metadata) if getattr(metadata, field.name) is None]} missing"
            )
