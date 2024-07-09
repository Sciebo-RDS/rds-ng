import typing

from common.py.utils.func import ExecutionCallbacks


class OSFRootInformationCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],  # TODO: Data type
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the root information API call.
    """
