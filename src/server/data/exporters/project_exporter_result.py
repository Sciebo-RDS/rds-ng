from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ProjectExporterResult:
    """
    Encapsulates the result of a project export.
    """

    mimetype: str

    data: bytes
