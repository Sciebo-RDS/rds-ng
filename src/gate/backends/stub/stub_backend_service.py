import time
import typing

from common.py.api import UpdateProjectFeaturesCommand, UpdateProjectFeaturesReply
from common.py.component import BackendComponent
from common.py.data.entities import clone_entity
from common.py.data.entities.features import ProjectFeature, ProjectFeatureID
from common.py.data.verifiers.project_features_verifier import ProjectFeaturesVerifier
from common.py.services import Service

from .stub_backend_service_context import StubBackendServiceContext
from .stub_utils import send_projects_list


def create_stub_backend_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api import (
        ListProjectsCommand,
        ListProjectsReply,
        CreateProjectCommand,
        CreateProjectReply,
        UpdateProjectCommand,
        UpdateProjectReply,
        DeleteProjectCommand,
        DeleteProjectReply,
    )
    from common.py.data.entities import Project
    from common.py.data.verifiers import ProjectVerifier

    svc = comp.create_service(
        "Stub Backend service", context_type=StubBackendServiceContext
    )

    # Project commands
    @svc.message_handler(ListProjectsCommand)
    def list_projects(msg: ListProjectsCommand, ctx: StubBackendServiceContext) -> None:
        ListProjectsReply.build(
            ctx.message_builder, msg, projects=ctx.storage_pool.project_storage.list()
        ).emit()

    @svc.message_handler(CreateProjectCommand)
    def create_project(
        msg: CreateProjectCommand, ctx: StubBackendServiceContext
    ) -> None:
        success = False
        message = ""

        project = Project(
            project_id=ctx.storage_pool.project_storage.next_id(),
            creation_time=time.time(),
            title=msg.title,
            description=msg.description,
            options=msg.options,
        )

        try:
            ProjectVerifier(project).verify_create()

            ctx.storage_pool.project_storage.add(project)
            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        CreateProjectReply.build(
            ctx.message_builder,
            msg,
            project_id=project.project_id,
            success=success,
            message=message,
        ).emit()

        send_projects_list(msg, ctx)

    @svc.message_handler(UpdateProjectCommand)
    def update_project(
        msg: UpdateProjectCommand, ctx: StubBackendServiceContext
    ) -> None:
        success = False
        message = ""

        if (
            project := ctx.storage_pool.project_storage.get(msg.project_id)
        ) is not None:
            try:
                project_upd = clone_entity(
                    project,
                    title=msg.title,
                    description=msg.description,
                    options=msg.options,
                )
                ProjectVerifier(project_upd).verify_update()

                ctx.storage_pool.project_storage.add(project_upd)
                success = True
            except Exception as exc:  # pylint: disable=broad-exception-caught
                message = str(exc)
        else:
            message = f"A project with ID {msg.project_id} was not found"

        UpdateProjectReply.build(
            ctx.message_builder,
            msg,
            project_id=msg.project_id,
            success=success,
            message=message,
        ).emit()

        send_projects_list(msg, ctx)

    @svc.message_handler(UpdateProjectFeaturesCommand)
    def update_project_features(
        msg: UpdateProjectFeaturesCommand, ctx: StubBackendServiceContext
    ) -> None:
        success = False
        message = ""

        if (
            project := ctx.storage_pool.project_storage.get(msg.project_id)
        ) is not None:
            try:
                project_features_upd = clone_entity(
                    project.features,
                    **msg.features.features_dict(
                        selected_features=msg.updated_features
                    ),
                )
                ProjectFeaturesVerifier(
                    project_features_upd, selected_features=msg.updated_features
                ).verify_update()

                project_upd = clone_entity(project, features=project_features_upd)

                ctx.storage_pool.project_storage.add(project_upd)
                success = True
            except Exception as exc:  # pylint: disable=broad-exception-caught
                message = str(exc)
        else:
            message = f"A project with ID {msg.project_id} was not found"

        UpdateProjectFeaturesReply.build(
            ctx.message_builder,
            msg,
            project_id=msg.project_id,
            updated_features=msg.updated_features if success else [],
            success=success,
            message=message,
        ).emit()

        send_projects_list(msg, ctx)

    @svc.message_handler(DeleteProjectCommand)
    def delete_project(
        msg: DeleteProjectCommand, ctx: StubBackendServiceContext
    ) -> None:
        success = False
        message = ""

        if (
            project := ctx.storage_pool.project_storage.get(msg.project_id)
        ) is not None:
            try:
                ProjectVerifier(project).verify_delete()

                ctx.storage_pool.project_storage.remove(project)
                success = True
            except Exception as exc:  # pylint: disable=broad-exception-caught
                message = str(exc)
        else:
            message = f"A project with ID {msg.project_id} was not found"

        DeleteProjectReply.build(
            ctx.message_builder,
            msg,
            project_id=msg.project_id,
            success=success,
            message=message,
        ).emit()

        send_projects_list(msg, ctx)

    # Add some initial data to the in-memory storage
    from .stub_data_connectors import fill_stub_data_connectors
    from .stub_data_projects import fill_stub_data_projects

    fill_stub_data_connectors()
    fill_stub_data_projects()

    return svc
