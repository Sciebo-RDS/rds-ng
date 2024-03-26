import time

from common.py.component import BackendComponent
from common.py.services import Service

from .tools import send_projects_list


def create_projects_service(comp: BackendComponent) -> Service:
    """
    Creates the projects service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.project import (
        ListProjectsCommand,
        ListProjectsReply,
        CreateProjectCommand,
        CreateProjectReply,
        UpdateProjectCommand,
        UpdateProjectReply,
        DeleteProjectCommand,
        DeleteProjectReply,
        UpdateProjectFeaturesCommand,
        UpdateProjectFeaturesReply,
    )
    from common.py.data.entities import clone_entity
    from common.py.data.entities.project import Project
    from common.py.data.verifiers.project import (
        ProjectVerifier,
        ProjectFeaturesVerifier,
    )

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Projects service", context_type=ServerServiceContext)

    @svc.message_handler(ListProjectsCommand)
    def list_projects(msg: ListProjectsCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, ListProjectsReply):
            return

        ListProjectsReply.build(
            ctx.message_builder,
            msg,
            projects=ctx.storage_pool.project_storage.filter_by_user(ctx.user.user_id),
        ).emit()

    @svc.message_handler(CreateProjectCommand)
    def create_project(msg: CreateProjectCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, CreateProjectReply, project_id=0):
            return

        success = False
        message = ""

        project = Project(
            project_id=ctx.storage_pool.project_storage.next_id(),
            user_id=ctx.user.user_id,
            creation_time=time.time(),
            resources_path=msg.resources_path,
            title=msg.title.strip(),
            description=msg.description.strip(),
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
    def update_project(msg: UpdateProjectCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, UpdateProjectReply, project_id=0):
            return

        success = False
        message = ""

        if (
            project := ctx.storage_pool.project_storage.get(msg.project_id)
        ) is not None:
            try:
                project_upd = clone_entity(
                    project,
                    title=msg.title.strip(),
                    description=msg.description.strip(),
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
        msg: UpdateProjectFeaturesCommand, ctx: ServerServiceContext
    ) -> None:
        if not ctx.ensure_user(
            msg, UpdateProjectFeaturesReply, project_id=0, updated_features=[]
        ):
            return

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

        # TODO:
        # send_projects_list(msg, ctx)

    @svc.message_handler(DeleteProjectCommand)
    def delete_project(msg: DeleteProjectCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, DeleteProjectReply, project_id=0):
            return

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

    return svc
