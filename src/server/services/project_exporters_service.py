import typing

from common.py.component import BackendComponent
from common.py.data.exporters import (
    ProjectExporterDescriptor,
    descriptor_from_project_exporter,
)
from common.py.services import Service

from ..data.exporters import ProjectExportersCatalog


def create_project_exporters_service(comp: BackendComponent) -> Service:
    """
    Creates the exporters service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from common.py.api.project import (
        ListProjectExportersCommand,
        ListProjectExportersReply,
        ExportProjectCommand,
        ExportProjectReply,
    )

    from .server_service_context import ServerServiceContext

    svc = comp.create_service(
        "Project exporters service", context_type=ServerServiceContext
    )

    @svc.message_handler(ListProjectExportersCommand)
    def list_exporters(
        msg: ListProjectExportersCommand, ctx: ServerServiceContext
    ) -> None:
        exporters: typing.List[ProjectExporterDescriptor] = []
        for _, exporter in ProjectExportersCatalog.items():
            exporters.append(descriptor_from_project_exporter(exporter))

        ListProjectExportersReply.build(
            ctx.message_builder, msg, exporters=exporters
        ).emit()

    @svc.message_handler(ExportProjectCommand)
    def export_project(msg: ExportProjectCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, ExportProjectReply, mimetype="", data=bytes()):
            return

        # TODO: Get project, exporter; initiate etc
        import time

        time.sleep(5)

        ExportProjectReply.build(
            ctx.message_builder,
            msg,
            mimetype="",
            data=bytes(),
            success=False,
            message="not done yet",
        ).emit()

    return svc
