import typing

from common.py.utils.func import ExecutionCallbacks

from .inveniordm_request_data import (
    InvenioRDMFileObject,
    InvenioRDMFileListObject,
    InvenioRDMProjectObject,
)


class InvenioRDMGetProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[InvenioRDMProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get project API call.
    """


class InvenioRDMCreateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[InvenioRDMProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the create project API call.
    """


class InvenioRDMUpdateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[InvenioRDMProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the update project API call.
    """


class InvenioRDMDeleteProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete project API call.
    """


class InvenioRDMGetFileListCallbacks(
    ExecutionCallbacks[
        typing.Callable[[InvenioRDMFileListObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get file list API call.
    """


class InvenioRDMUploadFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[InvenioRDMFileObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the upload file API call.
    """


class InvenioRDMDeleteFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete file API call.
    """


class InvenioRDMDeleteAllFilesCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete all files API call.
    """
