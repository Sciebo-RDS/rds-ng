import typing

from common.py.utils.func import ExecutionCallbacks

from .osf_request_data import (
    OSFFileListObject,
    OSFFileObject,
    OSFProjectObject,
    OSFStorageObject,
)


class OSFGetProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get project API call.
    """


class OSFCreateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the create project API call.
    """


class OSFUpdateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFProjectObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the update project API call.
    """


class OSFDeleteProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete project API call.
    """


class OSFGetStorageCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFStorageObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get storage API call.
    """


class OSFGetFileListCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFFileListObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get file list API call.
    """


class OSFUploadFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFFileObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the upload file API call.
    """


class OSFDeleteFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete file API call.
    """


class OSFDeleteAllFilesCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete all files API call.
    """
