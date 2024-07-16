import enum
import io
import typing

from ....data.entities.resource import Resource, ResourcesList
from ....utils.func import ExecutionCallbacks

ResourceBuffer = io.RawIOBase


class ResourcesTransmitterPrepareCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ResourcesList], None], typing.Callable[[str], None]
    ]
):
    """
    Callbacks used for transmitter preparation.
    """


class ResourcesTransmitterDownloadCallbacks(
    ExecutionCallbacks[
        typing.Callable[[Resource, ResourceBuffer], None],
        typing.Callable[[Resource, str], None],
    ]
):
    """
    Callbacks used for transmitter downloads.
    """

    class _CallbackType(enum.StrEnum):
        PROGRESS = "progress"
        ALL_DONE = "all_done"

    def progress(self, cb: typing.Callable[[Resource, int, int], None]) -> typing.Self:
        """
        Adds a *Progress* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance to allow call chaining.
        """
        self.assign(ResourcesTransmitterDownloadCallbacks._CallbackType.PROGRESS, cb)
        return self

    def all_done(self, cb: typing.Callable[[bool], None]) -> typing.Self:
        """
        Adds a *All Done* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance to allow call chaining.
        """
        self.assign(ResourcesTransmitterDownloadCallbacks._CallbackType.ALL_DONE, cb)
        return self

    def invoke_progress_callbacks(self, *args, **kwargs) -> None:
        """
        Invokes all *Progress* callbacks.
        """
        self.invoke(
            ResourcesTransmitterDownloadCallbacks._CallbackType.PROGRESS,
            *args,
            **kwargs
        )

    def invoke_all_done_callbacks(self, *args, **kwargs) -> None:
        """
        Invokes all *All Done* callbacks.
        """
        self.invoke(
            ResourcesTransmitterDownloadCallbacks._CallbackType.ALL_DONE,
            *args,
            **kwargs
        )
