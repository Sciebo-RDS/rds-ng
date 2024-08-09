from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class MetadataParserQuery:
    id: str
    value: str


class MetadataParser:

    @staticmethod
    def filter_by_profile(
        profile_name: str | List, metadata: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        if isinstance(profile_name, str):
            profile_name = [profile_name]

        return list(
            filter(
                lambda y: any(
                    profile in map(lambda z: z[0], y["profiles"])
                    for profile in profile_name
                ),
                metadata,
            )
        )

    @staticmethod
    def getattr(metadata: List[Dict[str, Any]], query: MetadataParserQuery) -> Any:
        return next(
            (
                e["value"][query.value]
                for e in metadata
                if e["id"] == query.id and query.value in e["value"]
            ),
            None,
        )
