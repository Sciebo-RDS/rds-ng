from common.py.utils import ItemsCatalog

from common.py.data.exporters.project_exporter import ProjectExporter


@ItemsCatalog.define()
class ProjectExportersCatalog(ItemsCatalog[ProjectExporter]):
    """
    Global catalog of all project exporters.
    """
