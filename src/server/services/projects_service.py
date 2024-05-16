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
        MarkProjectLogbookSeenCommand,
        MarkProjectLogbookSeenReply,
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
        if not ctx.ensure_user(msg, ListProjectsReply, projects=[]):
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
            ProjectVerifier(project, ctx.user).verify_create()

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

            def _apply_update(proj: Project) -> Project:
                proj.title = msg.title.strip()
                proj.description = msg.description.strip()
                proj.options = msg.options
                return proj

            try:
                # Clone the project, applying the new settings, to only update the actual instance if everything is fine
                project_upd = _apply_update(clone_entity(project))
                ProjectVerifier(project_upd, ctx.user).verify_update()

                _apply_update(project)
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
                ProjectVerifier(project, ctx.user).verify_update()
                ProjectFeaturesVerifier(
                    msg.features, selected_features=msg.updated_features
                ).verify_update()

                from common.py.data.entities.project import (
                    apply_project_features_update,
                )

                apply_project_features_update(
                    project, msg.features, msg.updated_features
                )
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

    @svc.message_handler(MarkProjectLogbookSeenCommand)
    def mark_project_logbook_seen(
        msg: MarkProjectLogbookSeenCommand, ctx: ServerServiceContext
    ) -> None:
        if not ctx.ensure_user(msg, MarkProjectLogbookSeenReply):
            return

        from common.py.data.entities.project.logbook import find_logbook_by_type

        from .tools import send_project_logbook

        success = False
        message = ""

        if msg.mark_all:
            success = True

            for project in ctx.storage_pool.project_storage.filter_by_user(
                ctx.user.user_id
            ):
                send_logbook = False

                for record in find_logbook_by_type(project, msg.logbook_type):
                    if not record.seen:
                        record.seen = True
                        send_logbook = True

                if send_logbook:
                    send_project_logbook(msg, ctx, project)
        else:
            if (
                project := ctx.storage_pool.project_storage.get(msg.project_id)
            ) is not None:
                from common.py.data.entities.project.logbook import (
                    find_logbook_record_by_id,
                )

                ProjectVerifier(project, ctx.user).verify_update()

                if (
                    record := find_logbook_record_by_id(
                        find_logbook_by_type(project, msg.logbook_type), msg.record
                    )
                ) is not None:
                    record.seen = True
                    success = True

                    send_project_logbook(msg, ctx, project)
                else:
                    message = f"A logbook record with ID {msg.record} was not found"
            else:
                message = f"A project with ID {msg.project_id} was not found"

        MarkProjectLogbookSeenReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
        ).emit()

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
                ProjectVerifier(project, ctx.user).verify_delete()

                for job in ctx.storage_pool.project_job_storage.filter_by_project(
                    project.project_id
                ):
                    ctx.storage_pool.project_job_storage.remove(job)

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
