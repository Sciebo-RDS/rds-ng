import json
import pathlib
import typing
from pathlib import PosixPath

from ..properties import ProfileID, PropertyProfile

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


def filter_containers_by_roles(
    containers: MetadataProfileContainerList,
    roles: typing.List[MetadataProfileContainer.Role],
) -> MetadataProfileContainerList:
    """
    Gets all containers from a list matching the specified role.

    Args:
        containers: The list of containers.
        roles: The roles to match.

    Returns:
        List of all matching containers.
    """
    return [container for container in containers if container.role in roles]


def filter_containers(
    containers: MetadataProfileContainerList,
    *,
    category: str,
    roles: typing.List[MetadataProfileContainer.Role],
) -> MetadataProfileContainerList:
    """
    Gets all containers from a list matching the specified category and role.

    Args:
        containers: The list of containers.
        category: The category to match.
        roles: The roles to match.

    Returns:
        List of all matching containers.
    """

    return [
        container
        for container in containers
        if container.category == category and container.role in roles
    ]


def filter_containers_ex(
    containers: MetadataProfileContainerList,
    *,
    category: str,
    roles: typing.List[MetadataProfileContainer.Role],
    enabled_profiles: typing.List[ProfileID],
) -> MetadataProfileContainerList:
    """
    Gets all containers from a list matching the specified category and role.

    Args:
        containers: The list of containers.
        category: The category to match.
        roles: The roles to match.
        enabled_profiles: A list of user-enabled optional profiles.

    Returns:
        List of all matching containers.
    """

    filtered_containers: MetadataProfileContainerList = []
    for container in containers:
        if container.category == category and container.role in roles:
            if is_container_selected(container, enabled_profiles=enabled_profiles):
                filtered_containers.append(container)
    return filtered_containers


def containers_from_folder(
    folder: pathlib.PosixPath, *, default_category: str | None = None
) -> MetadataProfileContainerList:
    """
    Loads all profiles from the specified folder. The files are separated into distinct folders that
    represent the various profile categories. Within each category folder, subfolders represent the
    profile roles, and each role folder can hold an arbitrary number of profiles.

    Args:
        folder: The folder to load.
        default_category: A default category for all profiles, skipping category directory parsing.

    Returns:
        A list of all loaded profiles.
    """

    containers: MetadataProfileContainerList = []

    def _read_role_folder(category: str, path: PosixPath) -> None:
        for role_item in path.iterdir():
            if role_item.is_dir():
                role = role_item.name

                if role not in MetadataProfileContainer.Role:
                    return

                # All .json files are loaded as profiles
                for profile_file in role_item.iterdir():
                    profile_file = typing.cast(PosixPath, profile_file)

                    if (
                        profile_file.is_file()
                        and profile_file.suffix.lower() == ".json"
                    ):
                        try:
                            with open(profile_file, "r") as file:
                                profile = PropertyProfile.from_dict(json.load(file))
                                containers.append(
                                    MetadataProfileContainer(
                                        category=category,
                                        role=typing.cast(
                                            MetadataProfileContainer.Role, role
                                        ),
                                        profile=profile,
                                    )
                                )
                        except:  # pylint: disable=bare-except
                            pass

    if default_category is not None:
        _read_role_folder(default_category, folder)
    else:
        # All subfolders in the given folder are treated as categories
        for category_item in folder.iterdir():
            category_item = typing.cast(pathlib.PosixPath, category_item)
            if category_item.is_dir():
                _read_role_folder(category_item.name, category_item)

    return containers


def is_container_selected(
    container: MetadataProfileContainer, *, enabled_profiles: typing.List[ProfileID]
) -> bool:
    """
    Checks whether a profile (container) is selected - either since it is a default one or the user has enabled it.

    Args:
        container: The container to check.
        enabled_profiles: All user-enabled profiles.
    """
    if container.role == MetadataProfileContainer.Role.DEFAULT:
        return True
    elif container.role == MetadataProfileContainer.Role.OPTIONAL:
        for profile_id in enabled_profiles:
            if (
                profile_id[0] == container.profile.metadata.id[0]
                and profile_id[1] == container.profile.metadata.id[1]
            ):
                return True

    return False
