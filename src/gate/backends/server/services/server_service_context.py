from common.py.core.messaging import Channel

from ....services import GateServiceContext


class ServerServiceContext(GateServiceContext):
    """
    Service context specific to the server backend.
    """

    @property
    def server_channel(self) -> Channel:
        """
        Retrieves the global server channel.

        Returns:
            The global server channel, if any.

        Raises:
            RuntimeError: If no server channel has been set.
        """
        from gate.backends.server.networking.server_channel import server_channel

        return server_channel()
