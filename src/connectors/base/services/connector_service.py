from common.py.component import BackendComponent
from common.py.services import Service

_ANNOUNCE_INTERVAL = 3600  # Once per hour


def create_connector_service(comp: BackendComponent) -> Service:
    """
    Creates the main connector service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.component import ComponentProcessEvent

    from .connector_service_context import ConnectorServiceContext

    svc = comp.create_service("Connector service", context_type=ConnectorServiceContext)

    svc.state.last_announce = 0.0

    @svc.message_handler(ComponentProcessEvent)
    def announce(msg: ComponentProcessEvent, ctx: ConnectorServiceContext) -> None:
        if msg.timestamp - svc.state.last_announce >= _ANNOUNCE_INTERVAL:
            from common.py.api.connector import ConnectorAnnounceEvent

            from ..component import ConnectorComponent

            info = ConnectorComponent.instance().connector_info
            ConnectorAnnounceEvent.build(
                ctx.message_builder,
                connector_id=info.connector_id,
                name=info.name,
                description=info.description,
                category=info.category,
                options=info.options,
                logos=info.logos,
                metadata_profile=info.metadata_profile,
            ).emit(ctx.remote_channel)

            svc.state.last_announce = msg.timestamp

    return svc
