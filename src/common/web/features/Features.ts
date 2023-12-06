import logging from "../core/logging/Logging";
import { type Constructable } from "../utils/Types";
import { DataManagementPlanFeature } from "./DataManagementPlanFeature";
import { MetadataFeature } from "./MetadataFeature";
import { ProjectFeature } from "./ProjectFeature";
import { findPanelLoader, type ProjectFeaturePanelLoaders } from "./ProjectFeaturePanelLoader";
import { ProjectFeaturesCatalog } from "./ProjectFeaturesCatalog";
import { SummaryFeature } from "./SummaryFeature";

/**
 * Registers all available project features.
 *
 * When adding a new project feature, always register it here.
 *
 * @param panelLoaders - Optional panel loaders to provide panels for the various features.
 */
export function registerProjectFeatures(panelLoaders?: ProjectFeaturePanelLoaders): void {
    interface ConstructableFeature extends Constructable<ProjectFeature> {
        FeatureID: string;
    }

    function registerFeature(feature: ConstructableFeature): void {
        ProjectFeaturesCatalog.registerItem(feature.FeatureID, new feature(findPanelLoader(feature.FeatureID, panelLoaders)));
    }

    // New project features go here; the order in which they are added also define the order of their panels
    registerFeature(MetadataFeature);
    registerFeature(DataManagementPlanFeature);
    registerFeature(SummaryFeature);

    // Print all available features for debugging purposes
    const names = Object.keys(ProjectFeaturesCatalog.items).map((item) => `${ProjectFeaturesCatalog.items[item].displayName} (${item})`);
    logging.debug(`Registered project features: ${names.join("; ")}`);
}
