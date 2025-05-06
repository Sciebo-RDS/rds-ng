import typing

# pylint: disable=invalid-name
CallbackType = typing.TypeVar("CallbackType")


class CallbacksStack:
    """
    Helper class for running arbitrary callbacks.
    """
    
    def __init__(self):
        self._callbacks: typing.Dict[str, typing.List[CallbackType]] = {}
        
    def assign(self, key: str, cb: CallbackType) -> typing.Self:
        """
        Assigns a new callback for the specified key.
        
        Args:
            key: The key of the callback stack.
            cb: The callback.

        Returns:
            This instance for easy chaining.
        """
        if key not in self._callbacks:
            self._callbacks[key] = []

        self._callbacks[key].append(cb)
        return self

    def invoke(self, key: str, *args, **kwargs) -> None:
        """
        Invokes all callbacks for the specified key.
        
        Args:
            key: The key of the callback stack.
        """
        if key not in self._callbacks:
            return

        for cb in self._callbacks[key]:
            if callable(cb):
                cb(*args, **kwargs)

    def reset(self) -> None:
        """
        Removecs all callbacks.
        """
        self._callbacks = {}
        
    def callbacks(self, key: str) -> typing.List[CallbackType]:
        """
        Gets all callbacks associated with the given key.
        
        Args:
            key: The key of the callback stack.

        Returns:
            List of callbacks.
        """
        return self._callbacks[key] if key in self._callbacks else []
