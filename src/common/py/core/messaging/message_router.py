from .message import Message
from .meta import MessageMetaInformation
from ...utils import UnitID


class MessageRouter:
    """
    Message routing rules and logic.

    When a message enters the message bus, it is first checked for its validity.
    Afterwards, the router decides through which channels (local, remote) it needs to be sent.
    """

    class RoutingError(RuntimeError):
        """
        Represents errors during routing validation.
        """

    def __init__(self, comp_id: UnitID, api_key: str):
        """
        Args:
            comp_id: The component id (required to decide whether we match a given direct target).
            api_key: The API key.
        """
        self._comp_id = comp_id

        self._api_key = api_key

    def verify_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        """
        Verifies whether a message may enter the message bus.

        Args:
            msg: The message that wants to enter the network engine.
            msg_meta: The message meta information.

        Raises:
            RoutingError: In case the message is not valid to enter the message bus.
        """
        if msg.is_protected():
            self._verify_protected_message(msg)

        if msg.target.is_local:
            self._verify_local_message(msg, msg_meta)
        if msg.target.is_direct:
            self._verify_direct_message(msg, msg_meta)

    def check_local_routing(
        self, msg: Message, msg_meta: MessageMetaInformation
    ) -> bool:
        """
        Checks if the message should be routed locally.

        Args:
            msg: The message.
            msg_meta: The message meta information.

        Returns:
            Whether local routing should happen.
        """
        if msg.target.is_local:
            return True
        if msg.target.is_direct:
            # A direct message that has made it to the message bus either stems from this component or is targeted to it
            # If it is targeted to this component, it needs to be dispatched locally
            return msg.target.target_id.equals(self._comp_id)

        return False

    def check_remote_routing(
        self, msg: Message, msg_meta: MessageMetaInformation
    ) -> bool:
        """
        Checks if the message should be routed remotely.

        Args:
            msg: The message.
            msg_meta: The message meta information.

        Returns:
            Whether remote routing should happen.
        """
        return (
            not msg.target.is_local
            and msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
        )

    def _verify_protected_message(self, msg: Message) -> None:
        if msg.api_key == "":
            raise MessageRouter.RoutingError(
                "Protected message without an API key received"
            )
        if self._api_key == "":
            raise MessageRouter.RoutingError(
                "No API key has been set in the component configuration"
            )

        if msg.api_key != self._api_key:
            raise MessageRouter.RoutingError("API key mismatch")

    def _verify_local_message(
        self, msg: Message, msg_meta: MessageMetaInformation
    ) -> None:
        if msg_meta.entrypoint != MessageMetaInformation.Entrypoint.LOCAL:
            raise MessageRouter.RoutingError(
                "Local message entering from a non-local location received"
            )

    def _verify_direct_message(
        self, msg: Message, msg_meta: MessageMetaInformation
    ) -> None:
        if msg.target.target_id is None:
            raise MessageRouter.RoutingError("Direct message without a target received")

        if (
            msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL
            and msg.target.target_id.equals(self._comp_id)
        ):
            raise MessageRouter.RoutingError(
                "Message coming from this component directed to self"
            )
        if (
            msg_meta.entrypoint != MessageMetaInformation.Entrypoint.LOCAL
            and not msg.target.target_id.equals(self._comp_id)
        ):
            raise MessageRouter.RoutingError(
                "Message coming from another component not directed to this component"
            )
