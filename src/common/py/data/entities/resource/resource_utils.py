import pathlib

from .resource import Resource
from .resources_list import ResourcesList, ResourceFiles, ResourceFolders


def resources_list_from_syspath(
    path: str,
    *,
    include_folders: bool = True,
    include_files: bool = True,
    recursive: bool = True
) -> ResourcesList:
    """
    Generates a *ResourcesList* from a system path.

    Args:
        path: The root path.
        include_folders: Whether to list folders (if this is set to false, no recursion will occur independent of `recursive`).
        include_files: Whether to list files.
        recursive: Whether to recursively process all sub-folders as well.

    Returns:
        A *ResourcesList* containing all contained files and folders.
    """

    def _process_path(
        root_path: pathlib.Path, *, process_resource: bool
    ) -> ResourcesList:
        folders: ResourceFolders = []
        files: ResourceFiles = []
        total_size: int = 0

        if process_resource:
            for child_path in root_path.iterdir():
                if child_path.is_dir() and include_folders:
                    path_resources = _process_path(
                        child_path, process_resource=recursive
                    )
                    folders.append(path_resources)
                    total_size += path_resources.resource.size
                elif child_path.is_file() and include_files:
                    file_size = child_path.stat().st_size
                    files.append(
                        Resource(
                            filename=str(child_path),
                            basename=child_path.name,
                            type=Resource.Type.FILE,
                            size=file_size,
                        )
                    )
                    total_size += file_size

        return ResourcesList(
            resource=Resource(
                filename=str(root_path),
                basename=root_path.name,
                type=Resource.Type.FOLDER,
                size=total_size,
            ),
            folders=folders,
            files=files,
        )

    return _process_path(pathlib.Path(path).resolve(), process_resource=True)
