import pathlib


def relativize_path(path: str, root: str) -> str:
    """
    Makes path relative to root, but keeps the new path absolute.
    
    Args:
        path: The full path.
        root: The root path.

    Returns:
        The relative-absolute path.
    """
    if root == "" or root == "/":
        return path
    
    rel_path = str(
        pathlib.PurePosixPath(path).relative_to(root)
    )
    if not rel_path.startswith("/"):
        rel_path = "/" + rel_path
    return rel_path
