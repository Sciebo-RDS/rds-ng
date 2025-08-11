import { Connector } from "../connector/Connector";
import { findConnectorByInstanceID } from "../connector/ConnectorInstanceUtils";
import { type MetadataProfileContainerList, MetadataProfileContainerRole } from "../metadata/MetadataProfileContainer";
import { filterContainers, filterContainersByRoles } from "../metadata/MetadataProfileContainerUtils";
import { UserSettings } from "../user/UserSettings";
import { Project, type ProjectID } from "./Project";

/**
 * Searches for a project by its ID within a list of projects.
 *
 * @param projects - The list of projects.
 * @param projectID - The project to search for.
 *
 * @returns - The found project or **undefined** otherwise.
 */
export function findProjectByID(projects: Project[], projectID: ProjectID): Project | undefined {
    return projects.find((project) => project.project_id == projectID);
}

/**
 * Checks if a connector is activated and valid for a given project.
 *
 * @param project - The project.
 * @param userSettings - The user settings.
 * @param connector - The connector to check.
 * @param connectors - A list of all known connectors.
 */
export function isConnectorActivated(project: Project, userSettings: UserSettings, connector: Connector, connectors: Connector[]): boolean {
    return !!userSettings.connector_instances.find((instance) => {
        if (project.options.use_all_connector_instances) {
            return instance.connector_id == connector.connector_id;
        } else {
            return !!project.options.active_connector_instances.find((instanceID) => {
                const resolvedConnector = findConnectorByInstanceID(connectors, userSettings.connector_instances, instanceID);
                return resolvedConnector && resolvedConnector.connector_id == connector.connector_id;
            });
        }
    });
}

/**
 * Gets all optional profiles for a specific feature of a project.
 * @param project - The project.
 * @param userSettings - The user settings.
 * @param connectors - A list of all known connectors.
 * @param profiles - A list of all metadata profiles.
 * @param featureID - The project feature ID.
 */
export function getOptionalMetadataProfiles(
    project: Project,
    userSettings: UserSettings,
    connectors: Connector[],
    profiles: MetadataProfileContainerList,
    featureID: string
): MetadataProfileContainerList {
    const optionalProfiles: MetadataProfileContainerList = [];

    for (const profile of filterContainers(profiles, featureID, [MetadataProfileContainerRole.Optional])) {
        optionalProfiles.push(profile);
    }

    connectors.forEach((connector) => {
        if (isConnectorActivated(project, userSettings, connector, connectors)) {
            for (const profile of filterContainersByRoles(connector.metadata_profiles, [MetadataProfileContainerRole.Optional])) {
                optionalProfiles.push(profile);
            }
        }
    });

    return optionalProfiles;
}
