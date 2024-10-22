from common.py.api import GetMetadataProfilesCommand, GetMetadataProfilesReply
from common.py.services import Service

from .server_service_context import ServerServiceContext
from ..component import ServerComponent


def create_metadata_service(comp: ServerComponent) -> Service:
    """
    Creates the session service that handles all metadata/profiles messages.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    svc = comp.create_service("Metadata service", context_type=ServerServiceContext)

    @svc.message_handler(GetMetadataProfilesCommand)
    def server_timeout(
        msg: GetMetadataProfilesCommand, ctx: ServerServiceContext
    ) -> None:
        GetMetadataProfilesReply.build(
            ctx.message_builder, msg, profiles=comp.server_data.profile_containers
        ).emit()

    return svc
