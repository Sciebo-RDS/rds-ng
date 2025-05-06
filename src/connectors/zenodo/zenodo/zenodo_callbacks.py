import typing

from common.py.utils.func import ExecutionCallbacks

from .zenodo_request_data import (
    ZenodoFileObject,
    ZenodoFileListObject,
    ZenodoProjectObject,
)


class ZenodoGetProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ZenodoProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get project API call.
    """


class ZenodoCreateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ZenodoProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the create project API call.
    """


class ZenodoUpdateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ZenodoProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the update project API call.
    """


class ZenodoDeleteProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete project API call.
    """


class ZenodoGetFileListCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ZenodoFileListObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get file list API call.
    """


class ZenodoUploadFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[ZenodoFileObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the upload file API call.
    """


class ZenodoDeleteFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete file API call.
    """


class ZenodoDeleteAllFilesCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete all files API call.
    """
