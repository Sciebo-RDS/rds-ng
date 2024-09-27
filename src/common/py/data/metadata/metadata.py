from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Dict, List


@dataclass
class Metadata(ABC):

    def __iter__(self):
        return (getattr(self, field.name) for field in fields(self))


class MetadataCreator(ABC):

    @abstractmethod
    def create(metadata: List[Dict[str, Any]]) -> Metadata:
        pass

    def validate(metadata: Metadata) -> None:
        if not all(metadata):
            raise ValueError(
                f"Invalid metadata, property {[field.name for field in fields(metadata) if getattr(metadata, field.name) == None or getattr(metadata, field.name) == '']} missing"
            )
