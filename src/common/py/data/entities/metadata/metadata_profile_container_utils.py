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
