import pathlib

from .resources_list import ResourcesList, ResourceFiles, ResourceFolders


def resources_list_from_syspath(
    path: str,
    *,
    include_files: bool = True,
    include_folders: bool = True,
    recursive: bool = True
) -> ResourcesList:
    """
    Generates a *ResourcesList* from a system path.

    Args:
        path: The root path.
        include_files: Whether to list files.
        include_folders: Whether to list folders (if this is set to false, no recursion will occur independent of `recursive`).
        recursive: Whether to recursively process all sub-folders as well.

    Returns:
        A *ResourcesList* containing all contained files and folders.
    """

    def _process_path(root_path: pathlib.Path) -> ResourcesList:
        folders: ResourceFolders = {}
        files: ResourceFiles = []

        for child_path in root_path.iterdir():
            if child_path.is_dir() and include_folders:
                folders[str(child_path)] = (
                    _process_path(child_path) if recursive else None
                )
            elif child_path.is_file() and include_files:
                files.append(str(child_path))

        return ResourcesList(resource=str(root_path), folders=folders, files=files)

    return _process_path(pathlib.Path(path).resolve())
