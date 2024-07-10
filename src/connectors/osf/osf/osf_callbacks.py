import typing

from common.py.utils.func import ExecutionCallbacks


class OSFCreateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[typing.Any], None],
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the root information API call.
    """
