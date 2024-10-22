import typing

from common.py.data.exporters import ProjectExporterDescriptor
from common.py.services import Service

from ..component import ServerComponent
from ..data.exporters import ProjectExportersCatalog


def create_project_exporters_service(comp: ServerComponent) -> Service:
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
            exporters.append(exporter.descriptor)

        ListProjectExportersReply.build(
            ctx.message_builder, msg, exporters=exporters
        ).emit()

    @svc.message_handler(ExportProjectCommand)
    def export_project(msg: ExportProjectCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, ExportProjectReply, mimetype="", data=bytes()):
            return

        def _reply(
            *,
            mimetype: str = "",
            data: bytes = bytes(),
            success: bool = True,
            message: msg = "",
        ) -> None:
            ExportProjectReply.build(
                ctx.message_builder,
                msg,
                mimetype=mimetype,
                data=data,
                success=success,
                message=message,
            ).emit()

        if (project := ctx.storage_pool.project_storage.get(msg.project_id)) is None:
            _reply(
                success=False,
                message=f"A project with ID {msg.project_id} was not found",
            )
            return

        if (exporter := ProjectExportersCatalog.find_item(msg.exporter)) is None:
            _reply(
                success=False,
                message=f"A project exporter with ID {msg.exporter} was not found",
            )
            return

        try:
            result = exporter.export(project, msg.scope)
            _reply(mimetype=result.mimetype, data=result.data)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            _reply(success=False, message=str(exc))

    return svc
