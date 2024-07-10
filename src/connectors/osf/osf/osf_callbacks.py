import typing

from common.py.utils.func import ExecutionCallbacks

from .osf_request_data import OSFFileData, OSFProjectData, OSFStorageData


class OSFCreateProjectCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFProjectData], None],
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the create project API call.
    """


class OSFGetStorageCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFStorageData], None],
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the get storage API call.
    """


class OSFUploadFileCallbacks(
    ExecutionCallbacks[
        typing.Callable[[OSFFileData], None],
        typing.Callable[[str], None],
    ]
):
    """
    Callbacks for the upload file API call.
    """
