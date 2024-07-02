import pathlib
import typing

from .resource import Resource
from .resources_list import ResourcesList, ResourceFiles, ResourceFolders


def resources_list_from_syspath(
    path: str,
    *,
    include_folders: bool = True,
    include_files: bool = True,
    recursive: bool = True,
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


def search_resources_list(resources: ResourcesList, path: str) -> ResourcesList:
    """
    Searches for a folder path within a resources list.

    Args:
        resources: The resources list to search.
        path: The path to search for.

    Returns:
        The found (nested) resources list, if any.

    Raises:
        ValueError: If the path could not be found.
    """
    if path == "":
        return resources

    root = pathlib.Path(path)

    def _search(resources_list: ResourcesList) -> ResourcesList | None:
        if pathlib.Path(resources_list.resource.filename) == root:
            return resources_list

        for folder in resources_list.folders:
            if found := _search(folder):
                return found
        else:
            return None

    if sublist := _search(resources):
        return sublist
    else:
        raise ValueError(f"The path '{path}' could not be found")


def filter_resources_list(
    resources: ResourcesList,
    *,
    include_folders: bool = True,
    include_files: bool = True,
) -> ResourcesList:
    """
    Filters a resource list.

    Args:
        resources: The list to filter.
        include_folders: Whether to include folders.
        include_files: Whether to include files.

    Returns:
        The filtered list.
    """
    from .. import clone_entity

    filtered_resources = clone_entity(resources)

    def _filter(resources_list: ResourcesList):
        if not include_files:
            resources_list.files.clear()

        if include_folders:
            for folder in resources_list.folders:
                _filter(folder)
        else:
            resources_list.folders.clear()

    _filter(filtered_resources)
    return filtered_resources


def files_list_from_resources_list(resources: ResourcesList) -> typing.List[Resource]:
    """
    Converts a resources list into a flat list of all included files.

    Args:
        resources: The resources list.

    Returns:
        The flattened files list.
    """
    files_list: typing.List[Resource] = []

    def _process_resources_list(resources_list: ResourcesList) -> None:
        nonlocal files_list

        files_list += resources_list.files

        for sub_list in resources_list.folders:
            _process_resources_list(sub_list)

    _process_resources_list(resources)
    return files_list
