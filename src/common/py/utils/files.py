import mimetypes
import pathlib

mimetypes.init()


def get_mime_type(filename: str) -> str:
    """
    Retrieves the MIME type based on the filename's extension.
    
    Args:
        filename: The filename.

    Returns:
        The MIME type, if any.
    """
    path = pathlib.PurePosixPath(filename)
    ext = path.suffix
    if ext in mimetypes.types_map:
        return mimetypes.types_map[ext]
    return ""
