from common.py.component import BackendComponent
from common.py.core.logging import info
from common.py.data.entities.authorization import AuthorizationSettings
from common.py.services import Service
from common.py.utils import EntryGuard

_ANNOUNCE_INTERVAL = 1.0 * 60  # Once per minute


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

    @svc.message_handler(ComponentProcessEvent, is_async=True)
    def announce(msg: ComponentProcessEvent, ctx: ConnectorServiceContext) -> None:
        with EntryGuard("announce") as guard:
            if not guard.can_execute:
                return

            if msg.timestamp - svc.state.last_announce >= _ANNOUNCE_INTERVAL:
                from common.py.api.connector import ConnectorAnnounceEvent

                from ..component import ConnectorComponent
                from ..integration.authorization.strategies import (
                    create_authorization_strategy_configuration,
                )
                from ..settings import AuthorizationSettingIDs

                strategy = ctx.config.value(AuthorizationSettingIDs.STRATEGY)
                strategy_config = create_authorization_strategy_configuration(
                    strategy, ctx.config
                )
                con_info = ConnectorComponent.instance().connector_info

                info(
                    "Sending connector announce",
                    scope="connectors",
                    id=con_info.connector_id,
                    name=con_info.name,
                    target=ctx.remote_channel,
                )

                ConnectorAnnounceEvent.build(
                    ctx.message_builder,
                    connector_id=con_info.connector_id,
                    name=con_info.name,
                    description=con_info.description,
                    category=con_info.category,
                    authorization_public=AuthorizationSettings(
                        strategy=strategy,
                        config=strategy_config.public_config,
                    ),
                    authorization_private=AuthorizationSettings(
                        strategy=strategy,
                        config=strategy_config.private_config,
                    ),
                    options=con_info.options,
                    logos=con_info.logos,
                    metadata_profiles=con_info.metadata_profiles,
                ).emit(ctx.remote_channel)

                svc.state.last_announce = msg.timestamp

    return svc
