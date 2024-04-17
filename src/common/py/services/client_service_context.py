from .service_context import ServiceContext
from ..core.messaging import Channel


class ClientServiceContext(ServiceContext):
    """
    A service context tailored towards working with a client connection.
    """

    _remote_channel: Channel | None = None

    @staticmethod
    def set_remote_channel(channel: Channel | None) -> None:
        """
        Sets (or resets) the remote channel.

        Args:
            channel: The remote or channel, or *None*.
        """
        ClientServiceContext._remote_channel = channel

    @property
    def remote_channel(self) -> Channel:
        """
        The remote channel.

        Raises:
            RuntimeError: If no connection exists.

        """
        if ClientServiceContext._remote_channel is None:
            raise RuntimeError(
                "Tried to access the remote channel without a connection"
            )

        return ClientServiceContext._remote_channel

    @property
    def is_connected(self) -> bool:
        """
        Whether the client is connected.
        """
        return ClientServiceContext._remote_channel is not None
