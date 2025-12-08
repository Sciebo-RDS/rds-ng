import typing

from common.py.utils.func import ExecutionCallbacks
from .dataverse_request_data import (
    DataverseCollectionObject,
    DataverseCreateDatasetObject,
    DataverseDatasetObject,
    DataverseDatasetVersionObject,
    DataverseFileListObject,
    DataverseFileObject,
    DataverseUserObject,
)


class DataverseGetUserCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseUserObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get user API call.
    """


class DataverseQueryCollectionCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseCollectionObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get collection API call.
    """


class DataverseGetDatasetCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseDatasetObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get dataset API call.
    """


class DataverseCreateCollectionCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseCollectionObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the create collection API call.
    """


class DataverseCreateDatasetCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseCreateDatasetObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the create dataset API call.
    """


class DataverseUploadFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseFileObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the upload file API call.
    """


class DataverseDeleteDatasetDraftCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete dataset API call.
    """


class DataverseUpdateDatasetCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseDatasetVersionObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the update dataset metadata API call.
    """


class DataverseDeleteAllFilesCallbacks(
    ExecutionCallbacks[
        typing.Callable[[], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the delete all files API call.
    """


class DataverseGetFileListCallbacks(
    ExecutionCallbacks[
        typing.Callable[[DataverseFileListObject], None],
        typing.Callable[[Exception], None],
    ]
):
    """
    Callbacks for the get file list API call.
    """
