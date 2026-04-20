from common.py.component import ComponentType, ComponentUnit
from common.py.core.messaging import Channel
from common.py.utils import UnitID


def get_server_channel() -> Channel:
    from common.py.services import ClientServiceContext

    # If a remote channel has been set in the client service context (Domo acts as a client), use that one.
    # Otherwise, direct messages to the server.
    channel = ClientServiceContext.get_remote_channel()
    return (
        channel
        if channel is not None
        else Channel.direct(UnitID(ComponentType.INFRASTRUCTURE, ComponentUnit.SERVER))
    )
