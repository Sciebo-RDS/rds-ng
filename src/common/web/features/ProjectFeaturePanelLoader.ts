import { type ProjectFeatureID } from "../data/entities/EntityTypes";

/**
 * Dynamic panel Vue component loader.
 */
export type ProjectFeaturePanelLoader = () => any;

/**
 * A mapping (feature ID to loader) for panel loaders.
 */
export type ProjectFeaturePanelLoaders = Record<ProjectFeatureID, ProjectFeaturePanelLoader>;

/**
 * Finds a panel loader for the given feature ID in the provided panel loaders.
 *
 * @param featureID - The feature ID to search the loader for.
 * @param loaders - The panel loaders; if no loaders are provided, `undefined` will be returned.
 *
 * @returns - The found panel loader or `undefined` otherwise.
 */
export function findPanelLoader(featureID: ProjectFeatureID, loaders?: ProjectFeaturePanelLoaders): ProjectFeaturePanelLoader | undefined {
    if (loaders && featureID in loaders) {
        return loaders[featureID];
    }
    return undefined;
}
