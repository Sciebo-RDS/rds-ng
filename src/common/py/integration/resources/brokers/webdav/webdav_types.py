from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True, kw_only=True)
class WebdavResource:
    """
    A resource information object as returned by WebDAV.
    """

    path: str
    isdir: bool

    size: int | None  # Only filled for files
    content_type: str | None  # Might not be provided by the underlying system
