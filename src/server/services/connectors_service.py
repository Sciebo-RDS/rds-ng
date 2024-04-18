from common.py.component import BackendComponent
from common.py.core.logging import info, debug
from common.py.data.entities.connector import Connector
from common.py.services import Service


def create_connectors_service(comp: BackendComponent) -> Service:
    """
    Creates the connectors service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.connector import (
        ConnectorAnnounceEvent,
        ListConnectorsCommand,
        ListConnectorsReply,
    )

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Connectors service", context_type=ServerServiceContext)

    @svc.message_handler(ConnectorAnnounceEvent)
    def connector_announce(
        msg: ConnectorAnnounceEvent, ctx: ServerServiceContext
    ) -> None:
        info(
            "Connector announce received",
            scope="connectors",
            id=msg.connector_id,
            name=msg.display_name,
        )

        connector = Connector(
            connector_id=msg.connector_id,
            name=msg.display_name,
            description=msg.description,
            logos=msg.logos,
            metadata_profile=msg.metadata_profile,
        )

        if (
            ex_connector := ctx.storage_pool.connector_storage.get(msg.connector_id)
        ) is not None:
            from common.py.data.entities.connector import apply_connector_update

            apply_connector_update(ex_connector, connector)
            debug(
                "Connector updated",
                scope="connectors",
                id=msg.connector_id,
                name=msg.display_name,
            )
        else:
            ctx.storage_pool.connector_storage.add(connector)
            debug(
                "Connector added",
                scope="connectors",
                id=msg.connector_id,
                name=msg.display_name,
            )

    @svc.message_handler(ListConnectorsCommand)
    def list_connectors(msg: ListConnectorsCommand, ctx: ServerServiceContext) -> None:
        ListConnectorsReply.build(
            ctx.message_builder,
            msg,
            connectors=ctx.storage_pool.connector_storage.list(),
        ).emit()

    return svc
