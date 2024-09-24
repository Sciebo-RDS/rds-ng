import typing

from common.py.core import logging

from .pdf import PDFExporter
from .project_exporters_catalog import ProjectExportersCatalog
from .rocrate import ROCrateExporter
from .text import TextExporter


def register_project_exporters() -> None:
    """
    Registers all available project exporters.

    When adding a new exporter, always register it here.
    """

    # New exporters go here
    ProjectExportersCatalog.register_item(TextExporter.ExporterID, TextExporter())
    ProjectExportersCatalog.register_item(PDFExporter.ExporterID, PDFExporter())
    ProjectExportersCatalog.register_item(ROCrateExporter.ExporterID, ROCrateExporter())

    # Print all available exporters for debugging purposes
    names: typing.List[str] = []
    for _, exporter in ProjectExportersCatalog.items():
        names.append(exporter.name)
    logging.debug(f"Registered project exporters: {'; '.join(names)}")
