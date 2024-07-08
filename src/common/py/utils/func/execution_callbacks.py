import enum
import typing

from .callbacks_stack import CallbacksStack

# pylint: disable=invalid-name
DoneCallbackType = typing.TypeVar("DoneCallbackType")
# pylint: disable=invalid-name
FailCallbackType = typing.TypeVar("FailCallbackType")


class ExecutionCallbacks(typing.Generic[DoneCallbackType, FailCallbackType], CallbacksStack):
    """
    Helper class for running 'Done' and 'Failed' callbacks during arbitrary executions.
    """
    
    class _CallbackType(enum.StrEnum):
        DONE = "done"
        FAIL = "fail"

    def done(self, cb: DoneCallbackType) -> typing.Self:
        """
        Adds a *Done* callback.

        Args:
            cb: The callback to add.
            
        Returns:
            This instance to allow call chaining.
        """
        self.assign(ExecutionCallbacks._CallbackType.DONE, cb)
        return self
    
    def failed(self, cb: FailCallbackType) -> typing.Self:
        """
        Adds a *Fail* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance to allow call chaining.
        """
        self.assign(ExecutionCallbacks._CallbackType.FAIL, cb)
        return self

    def invoke_done_callbacks(self, *args, **kwargs) -> None:
        """
        Invokes all *Done* callbacks.
        """
        self.invoke(ExecutionCallbacks._CallbackType.DONE, *args, **kwargs)
        
    def invoke_fail_callbacks(self, *args, **kwargs) -> None:
        """
        Invokes all *Fail* callbacks.
        """
        self.invoke(ExecutionCallbacks._CallbackType.FAIL, *args, **kwargs)

    @property
    def done_callbacks(self) -> typing.List[DoneCallbackType]:
        """
        All *Done* callbacks.
        """
        return self.callbacks(ExecutionCallbacks._CallbackType.DONE)
    
    @property
    def fail_callbacks(self) -> typing.List[FailCallbackType]:
        """
        All *Fail* callbacks.
        """
        return self.callbacks(ExecutionCallbacks._CallbackType.FAIL)
