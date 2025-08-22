import { type ProfileID } from "../../../ui/components/propertyeditor/PropertyProfile";
import { MetadataProfileContainer, type MetadataProfileContainerList, MetadataProfileContainerRole } from "./MetadataProfileContainer";

/**
 * Gets all containers from a list matching the specified category.
 *
 * @param containers - The list of containers.
 * @param category - The category to match.
 *
 * @returns - List of all matching containers.
 */
export function filterContainersByCategory(containers: MetadataProfileContainerList, category: string): MetadataProfileContainerList {
    return containers.filter((container) => container.category == category);
}

/**
 * Gets all containers from a list matching the specified role.
 *
 * @param containers - The list of containers.
 * @param roles - The roles to match.
 *
 * @returns - List of all matching containers.
 */
export function filterContainersByRoles(containers: MetadataProfileContainerList, roles: MetadataProfileContainerRole[]): MetadataProfileContainerList {
    return containers.filter((container) => roles.includes(container.role));
}

/**
 * Gets all containers from a list matching the specified category and role.
 *
 * @param containers - The list of containers.
 * @param category - The category to match.
 * @param roles - The roles to match.
 *
 * @returns - List of all matching containers.
 */
export function filterContainers(
    containers: MetadataProfileContainerList,
    category: string,
    roles: MetadataProfileContainerRole[]
): MetadataProfileContainerList {
    return containers.filter((container) => container.category == category && roles.includes(container.role));
}

/**
 * Checks whether a profile (container) is selected - either since it is a default one or the user has enabled it.
 *
 * @param container - The container to check.
 * @param enabledProfiles - All user-enabled profiles.
 */
export function isContainerSelected(container: MetadataProfileContainer, enabledProfiles: ProfileID[]): boolean {
    switch (container.role) {
        case MetadataProfileContainerRole.Default:
            return true;

        case MetadataProfileContainerRole.Optional:
            for (const profileID of enabledProfiles) {
                if (profileID[0] == container.profile.getName() && profileID[1] == container.profile.getVersion()) {
                    return true;
                }
            }
            return false;

        default:
            return false;
    }
}
