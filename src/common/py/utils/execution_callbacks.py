import typing

# pylint: disable=invalid-name
DoneCallbackType = typing.TypeVar("DoneCallbackType")
# pylint: disable=invalid-name
FailCallbackType = typing.TypeVar("FailCallbackType")


class ExecutionCallbacks(typing.Generic[DoneCallbackType, FailCallbackType]):
    """
    Helper class for running 'Done' and 'Failed' callbacks during arbitrary executions.
    """

    def __init__(self):
        self._done_callbacks: typing.List[DoneCallbackType] = []
        self._fail_callbacks: typing.List[FailCallbackType] = []
        
    def done(self, cb: DoneCallbackType) -> typing.Self:
        """
        Adds a *Done* callback.

        Args:
            cb: The callback to add.
            
        Returns:
            This instance to allow call chaining.
        """
        self._done_callbacks.append(cb)
        return self
    
    def failed(self, cb: FailCallbackType) -> typing.Self:
        """
        Adds a *Fail* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance to allow call chaining.
        """
        self._fail_callbacks.append(cb)
        return self

    def invoke_done_callbacks(self, *args, **kwargs) -> None:
        """
        Invokes all *Done* callbacks.
        """
        for cb in self._done_callbacks:
            cb(*args, **kwargs)
            
    def invoke_fail_callbacks(self, *args, **kwargs) -> None:
        """
        Invokes all *Fail* callbacks.
        """
        for cb in self._fail_callbacks:
            cb(*args, **kwargs)

    def reset(self) -> None:
        """
        Removecs all callbacks.
        """
        self._done_callbacks = []
        self._fail_callbacks = []

    @property
    def done_callbacks(self) -> typing.List[DoneCallbackType]:
        """
        All *Done* callbacks.
        """
        return self._done_callbacks
    
    @property
    def fail_callbacks(self) -> typing.List[FailCallbackType]:
        """
        All *Fail* callbacks.
        """
        return self._fail_callbacks
