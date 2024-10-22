import { MetadataProfileContainerList, MetadataProfileContainerRole } from "./MetadataProfileContainer";

/**
 * Gets all containers from a list matching the specified category.
 *
 * @param containers - The list of containers.
 * @param category - The category to match.
 *
 * @returns - List of all matching containers.
 */
export function filterContainersByCategory(containers: MetadataProfileContainerList, category: string): MetadataProfileContainerList {
    return containers.filter((container) => container.category == container);
}

/**
 * Gets all containers from a list matching the specified role.
 *
 * @param containers - The list of containers.
 * @param role - The role to match.
 *
 * @returns - List of all matching containers.
 */
export function filterContainersByRole(containers: MetadataProfileContainerList, role: MetadataProfileContainerRole): MetadataProfileContainerList {
    return containers.filter((container) => container.role == role);
}

/**
 * Gets all containers from a list matching the specified category and role.
 *
 * @param containers - The list of containers.
 * @param category - The category to match.
 * @param role - The role to match.
 *
 * @returns - List of all matching containers.
 */
export function filterContainers(containers: MetadataProfileContainerList, category: string, role: MetadataProfileContainerRole): MetadataProfileContainerList {
    return containers.filter((container) => container.category == category && container.role == role);
}
