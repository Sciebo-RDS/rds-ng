import json
import typing

PayloadData = typing.Any
Payload = typing.Dict[str, PayloadData]


class MessagePayload:
    """
    Class holding arbitrary payload data (as key-value pairs) of a message.
    """

    def __init__(self):
        self._payload: Payload = {}

    def set(self, key: str, data: PayloadData) -> None:
        """
        Sets a payload item.

        Args:
            key: The key of the item.
            data: The item data.
        """
        self._payload[key] = data

    def get(self, key: str) -> PayloadData | None:
        """
        Retrieves a payload item.

        Args:
            key: The key of the item.

        Returns:
            The item data or *None* otherwise.
        """
        return self._payload[key] if self.contains(key) else None

    def contains(self, key: str) -> bool:
        """
        Checks if an item exists.

        Args:
            key: The key of the item.
        """
        return key in self._payload

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def clear(self, key: str | None = None) -> None:
        """
        Removes an item or clears the entire payload.

        Args:
            key: The key of the item; if set to *None*, all items will be removed.
        """
        if key is not None:
            if self.contains(key):
                del self._payload[key]
        else:
            self._payload = {}

    def encode(self) -> Payload:
        """
        Encodes the payload for message passing.

        Returns:
            The encoded data.
        """
        return self._payload

    def decode(self, payload: Payload) -> None:
        """
        Decodes the payload from message passing.

        Args:
            payload: The incoming payload.
        """
        self._payload = payload

    def __str__(self) -> str:
        return json.dumps(self._payload)
