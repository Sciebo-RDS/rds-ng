import os.path
from typing import cast

from common.py.component import BackendComponent
from common.py.services import Service


def create_resources_service(comp: BackendComponent) -> Service:
    """
    Creates the resources service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.resource import ListResourcesCommand, ListResourcesReply

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Resources service", context_type=ServerServiceContext)

    @svc.message_handler(ListResourcesCommand)
    def list_resources(msg: ListResourcesCommand, ctx: ServerServiceContext) -> None:
        from common.py.data.entities.resource import Resource, ResourcesList

        if not ctx.ensure_user(
            msg, ListResourcesReply, resources=ResourcesList(resource=msg.root)
        ):
            return

        from ..settings import StorageSettingIDs

        success = False
        message = ""

        root = (
            msg.root
            if msg.root != ""
            else ctx.config.value(StorageSettingIDs.DEFAULT_ROOT_PATH)
        )
        resources = ResourcesList(
            resource=Resource(
                filename=root,
                basename=os.path.basename(root),
                type=Resource.Type.FOLDER,
            )
        )

        try:
            from common.py.data.entities.resource import (
                resources_list_from_syspath,
                search_resources_list,
                filter_resources_list,
            )

            # TODO: Temporary only
            stored_resources = ctx.session["resources"]
            resources = (
                filter_resources_list(
                    search_resources_list(
                        cast(
                            ResourcesList,
                            ResourcesList.schema().loads(stored_resources),
                        ),
                        root,
                    ),
                    include_folders=msg.include_folders,
                    include_files=msg.include_files,
                )
                if stored_resources
                else resources_list_from_syspath(
                    root,
                    include_folders=msg.include_folders,
                    include_files=msg.include_files,
                    recursive=msg.recursive,
                )
            )

            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        ListResourcesReply.build(
            ctx.message_builder,
            msg,
            resources=resources,
            success=success,
            message=message,
        ).emit()

    return svc
