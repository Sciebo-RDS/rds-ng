import json
import pathlib
import typing
from pathlib import PosixPath

from .metadata_profile_container import (
    MetadataProfileContainer,
    MetadataProfileContainerList,
)


def filter_containers_by_category(
    containers: MetadataProfileContainerList, category: str
) -> MetadataProfileContainerList:
    """
    Gets all containers from a list matching the specified category.

    Args:
        containers: The list of containers.
        category: The category to match.

    Returns:
        List of all matching containers.
    """
    return [container for container in containers if container.category == category]


def filter_containers_by_role(
    containers: MetadataProfileContainerList, role: MetadataProfileContainer.Role
) -> MetadataProfileContainerList:
    """
    Gets all containers from a list matching the specified role.

    Args:
        containers: The list of containers.
        role: The role to match.

    Returns:
        List of all matching containers.
    """
    return [container for container in containers if container.role == role]


def filter_containers(
    containers: MetadataProfileContainerList,
    *,
    category: str,
    role: MetadataProfileContainer.Role,
) -> MetadataProfileContainerList:
    """
    Gets all containers from a list matching the specified category and role.

    Args:
        containers: The list of containers.
        category: The category to match.
        role: The role to match.

    Returns:
        List of all matching containers.
    """

    return [
        container
        for container in containers
        if container.category == category and container.role == role
    ]


def containers_from_folder(folder: pathlib.PosixPath) -> MetadataProfileContainerList:
    """
    Loads all profiles from the specified folder. The files are separated into distinct folders that
    represent the various profile categories. Within each category folder, subfolders represent the
    profile roles, and each role folder can hold an arbitrary number of profiles.

    Args:
        folder: The folder to load.

    Returns:
        A list of all loaded profiles.
    """

    containers: MetadataProfileContainerList = []

    # All subfolders in the given folder are treated as categories
    for category_item in folder.iterdir():
        category_item = typing.cast(pathlib.PosixPath, category_item)
        if category_item.is_dir():
            category = category_item.name

            # All subfolders in a category are treated as roles
            for role_item in category_item.iterdir():
                role_item = typing.cast(PosixPath, role_item)

                if role_item.is_dir():
                    role = role_item.name

                    if role not in MetadataProfileContainer.Role:
                        continue

                    # All .json files are loaded as profiles
                    for profile_file in role_item.iterdir():
                        profile_file = typing.cast(PosixPath, profile_file)

                        if (
                            profile_file.is_file()
                            and profile_file.suffix.lower() == ".json"
                        ):
                            try:
                                with open(profile_file, "r") as file:
                                    containers.append(
                                        MetadataProfileContainer(
                                            category=category,
                                            role=typing.cast(
                                                MetadataProfileContainer.Role, role
                                            ),
                                            profile=json.load(file),
                                        )
                                    )
                            except:  # pylint: disable=bare-except
                                pass

    return containers
