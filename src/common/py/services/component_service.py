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
    from ..api.component import ComponentInformationEvent

    svc = comp.create_service("Component service")

    @svc.message_handler(ComponentInformationEvent)
    def component_information(
        msg: ComponentInformationEvent, ctx: ServiceContext
    ) -> None:
        # If this message is received through the client, we need to send our information in return to the server
        if ctx.is_entrypoint_client:
            data = BackendComponent.instance().data

            ComponentInformationEvent.build(
                ctx.message_builder,
                comp_id=data.comp_id,
                comp_name=data.name,
                comp_version=str(data.version),
                chain=msg,
            ).emit(Channel.direct(msg.comp_id))

    return svc
