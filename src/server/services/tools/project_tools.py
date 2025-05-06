import typing

from common.py.api import ProjectExternalStateEvent, ProjectExternalStateRenewalEvent
from common.py.core.logging import warning
from common.py.core.messaging import Message, Channel
from common.py.data.entities.connector import (
    ConnectorInstanceID,
    find_connector_by_instance_id,
)
from common.py.data.entities.project import Project
from common.py.data.exporters import ProjectExporterDescriptor, ProjectExporterID

from .. import ServerServiceContext
from ...networking.session import Session


def send_projects_list(
    msg: Message,
    ctx: ServerServiceContext,
    *,
    session: Session | None = None,
) -> None:
    """
    Sends the project list to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
        session: Override the user ID and target to use using a user's session.
    """
    from common.py.api.project import ProjectsListEvent

    if ctx.user is None and (session or session.user_token) is None:
        raise RuntimeError("Sending projects list without an authenticated user")

    ProjectsListEvent.build(
        ctx.message_builder,
        projects=ctx.storage_pool.project_storage.filter_by_user(
            session.user_token.user_id
            if session and session.user_token
            else ctx.user.user_id
        ),
        chain=msg,
    ).emit(Channel.direct(session.user_origin if session else msg.origin))


def send_project_external_states(
    msg: Message,
    ctx: ServerServiceContext,
    *,
    project: Project,
    session: Session | None = None,
) -> None:
    if ctx.user is None and (session or session.user_token) is None:
        raise RuntimeError(
            "Sending project external states without an authenticated user"
        )

    known_connector_instances: typing.List[ConnectorInstanceID] = []

    # Send all existing states of the touched project to the user
    for [
        _,
        connector_instance,
    ], state in ctx.session.user_data.volatile_project_states.get_states_by_project(
        project.project_id
    ).items():
        ProjectExternalStateEvent.build(
            ctx.message_builder,
            project_id=project.project_id,
            user_id=(
                session.user_token.user_id
                if session and session.user_token
                else ctx.user.user_id
            ),
            connector_instance=connector_instance,
            external_state=state.external_state,
            chain=msg,
        ).emit(
            Channel.direct(session.user_origin if session else ctx.session.user_origin)
        )

        known_connector_instances.append(connector_instance)

    # Issue renewal requests for missing connector instances
    for connector_instance in ctx.user.user_settings.connector_instances:
        if connector_instance.instance_id not in known_connector_instances:
            if (
                connector := find_connector_by_instance_id(
                    ctx.storage_pool.connector_storage.list(),
                    ctx.user.user_settings.connector_instances,
                    connector_instance.instance_id,
                )
            ) is not None:
                ProjectExternalStateRenewalEvent.build(
                    ctx.message_builder,
                    project=project,
                    connector_instance=connector_instance.instance_id,
                    user_token=ctx.session.user_token,
                ).emit(Channel.direct(connector.connector_address))


def create_auto_export_files(
    project: Project, *, exporter_ids: typing.List[ProjectExporterID]
) -> typing.Dict[str, bytes]:
    """
    Generates all auto-exported files for a project.

    Args:
        project: The project.
        exporter_ids: The IDs of the exporters to generate files with.

    Returns:
        The list of auto-generated files.
    """
    from ...data.exporters import ProjectExportersCatalog

    files: typing.Dict[str, bytes] = {}
    for _, exporter in ProjectExportersCatalog.items():
        if (
            exporter.exporter_id not in exporter_ids
            or ProjectExporterDescriptor.Capabilities.AUTO_EXPORT
            not in exporter.capabilities
        ):
            continue

        try:
            # For auto-export enabled exporters, the default_scope and default_filename are guaranteed to be set
            exporter_result = exporter.export(project, exporter.default_scope)
            files[exporter.default_filename] = exporter_result.data
        except Exception as exc:  # pylint: disable=broad-exception-caught
            warning(
                "An error occurred while auto-generating an export file",
                scope="job",
                exporter=exporter.exporter_id,
                error=str(exc),
            )

    return files
