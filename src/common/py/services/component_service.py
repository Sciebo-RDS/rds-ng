from semantic_version import Version

from .client_service_context import ClientServiceContext
from .service import Service, ServiceContext
from ..api import (
    API_PROTOCOL_VERSION,
    check_protocol_compatibility,
    ProtocolCompatibility,
)
from ..component import BackendComponent
from ..core import logging


def create_component_service(comp: BackendComponent) -> Service:
    """
    Creates the component service that handles various basic messaging tasks.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from ..core.messaging import Channel
    from ..api.component import ComponentInformationEvent, ComponentProcessEvent

    svc = comp.create_service("Component service")

    @svc.message_handler(ComponentInformationEvent, is_async=True)
    def component_information(
        msg: ComponentInformationEvent, ctx: ServiceContext
    ) -> None:
        # Notify of mismatching API protocol versions, which might lead to errors in network communication
        compat = check_protocol_compatibility(Version(msg.api_protocol))
        if compat == ProtocolCompatibility.NOT_COMPATIBLE:
            logging.error(
                "API major version mismatch; the affected components will not work together properly",
                scope="network",
                component=msg.comp_id,
                got=msg.api_protocol,
                want=str(API_PROTOCOL_VERSION),
            )
        elif compat == ProtocolCompatibility.MAYBE_COMPATIBLE:
            logging.warning(
                "API minor version mismatch; the affected components might not work together properly",
                scope="network",
                component=msg.comp_id,
                got=msg.api_protocol,
                want=str(API_PROTOCOL_VERSION),
            )

        # If this message is received through the client, we need to send our information in return to the server; we also store the channel of the server for client components
        if ctx.is_entrypoint_client:
            remote_channel = Channel.direct(msg.comp_id)
            ClientServiceContext.set_remote_channel(remote_channel)

            data = BackendComponent.instance().data
            ComponentInformationEvent.build(
                ctx.message_builder,
                comp_id=data.comp_id,
                comp_name=data.name,
                comp_version=str(data.version),
                chain=msg,
            ).emit(remote_channel)

    @svc.message_handler(ComponentProcessEvent, is_async=True)
    def component_process(msg: ComponentProcessEvent, ctx: ServiceContext) -> None:
        # Listen to this event to avoid complains about unhandled messages
        pass

    return svc
