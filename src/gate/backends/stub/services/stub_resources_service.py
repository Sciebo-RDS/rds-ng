import json
import os.path

from common.py.component import BackendComponent
from common.py.services import Service


def create_stub_resources_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend resources service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.resource import ListResourcesCommand, ListResourcesReply

    from .stub_service_context import StubServiceContext

    svc = comp.create_service("Resources service", context_type=StubServiceContext)

    @svc.message_handler(ListResourcesCommand)
    def list_resources(msg: ListResourcesCommand, ctx: StubServiceContext) -> None:
        from common.py.data.entities.resource import Resource, ResourcesList

        success = False
        message = ""

        root = msg.root if msg.root != "" else "/data"
        resources = ResourcesList(
            resource=Resource(
                filename=root,
                basename=os.path.basename(root),
                type=Resource.Type.FOLDER,
            )
        )

        try:
            from common.py.data.entities.resource.resource_utils import (
                resources_list_from_syspath,
            )
            from ....data.storage.session import SessionStorage

            # TODO: Temporary only
            stored_resources = SessionStorage().get_data(msg.origin, "resources", "")

            resources = (
                json.loads(stored_resources)
                if stored_resources != ""
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
