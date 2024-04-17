from .client_service_context import ClientServiceContext
from .service import Service, ServiceContext
from ..component import BackendComponent


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

    @svc.message_handler(ComponentInformationEvent)
    def component_information(
        msg: ComponentInformationEvent, ctx: ServiceContext
    ) -> None:
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

    @svc.message_handler(ComponentProcessEvent)
    def component_process(msg: ComponentProcessEvent, ctx: ServiceContext) -> None:
        # Listen to this event to avoid complains about unhandled messages
        pass

    return svc
