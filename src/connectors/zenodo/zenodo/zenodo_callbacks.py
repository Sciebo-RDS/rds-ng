import typing

from common.py.utils.func import ExecutionCallbacks

from .zenodo_request_data import ZenodoProjectData


class ZenodoCreateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ZenodoProjectData], None],
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the create project API call.
    """


class ZenodoDeleteProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the delete project API call.
    """
