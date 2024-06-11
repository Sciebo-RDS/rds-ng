import os.path
import typing
from typing import cast

from common.py.component import BackendComponent
from common.py.data.entities.resource import (
    Resource,
    ResourcesList,
    ResourcesBrokerToken,
)
from common.py.integration.resources.brokers import (
    create_resources_broker,
    ResourcesBroker,
)
from common.py.services import Service


def create_resources_service(comp: BackendComponent) -> Service:
    """
    Creates the resources service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.resource import (
        AssignResourcesBrokerCommand,
        AssignResourcesBrokerReply,
        ListResourcesCommand,
        ListResourcesReply,
    )

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Resources service", context_type=ServerServiceContext)

    def _create_broker(broker_token: ResourcesBrokerToken | None) -> ResourcesBroker:
        if broker_token is None:
            raise RuntimeError("No resources broker has been assigned")

        return create_resources_broker(comp, broker_token.broker, broker_token.config)

    @svc.message_handler(AssignResourcesBrokerCommand)
    def assign_resources_broker(
        msg: AssignResourcesBrokerCommand, ctx: ServerServiceContext
    ) -> None:
        if not ctx.ensure_user(msg, AssignResourcesBrokerReply):
            return

        success = False
        message = ""

        try:
            token = ResourcesBrokerToken(broker=msg.broker, config=msg.config)

            from common.py.data.verifiers.resource.resources_broker_token_verifier import (
                ResourcesBrokerTokenVerifier,
            )

            ResourcesBrokerTokenVerifier(token).verify_create()

            ctx.session.broker_token = token

            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        AssignResourcesBrokerReply.build(
            ctx.message_builder, msg, success=success, message=message
        ).emit()

    @svc.message_handler(ListResourcesCommand, is_async=True)
    def list_resources(msg: ListResourcesCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(
            msg, ListResourcesReply, resources=ResourcesList(resource=msg.root)
        ):
            return

        success = False
        message = ""

        resources = ResourcesList(
            resource=Resource(
                filename=msg.root,
                basename=os.path.basename(msg.root),
                type=Resource.Type.FOLDER,
            )
        )

        try:
            broker = _create_broker(ctx.session.broker_token)
            resources = broker.list_resources(
                msg.root,
                include_folders=msg.include_folders,
                include_files=msg.include_files,
                recursive=msg.recursive,
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
