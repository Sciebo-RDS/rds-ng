import typing

from common.py.data.entities.project import ProjectExternalState
from common.py.utils.func import ExecutionCallbacks


class ProjectExternalStateCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ProjectExternalState], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for external project state querying.
    """
