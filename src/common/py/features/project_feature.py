import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class ProjectFeature:
    """
    A project feature containing meta information describing a single project feature.
    """
