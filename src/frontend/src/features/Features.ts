import logging from "@common/core/logging/Logging";
import { ProjectFeaturesCatalog } from "@common/features/ProjectFeaturesCatalog";

import { DataManagementPlanFeature } from "@/features/DataManagementPlanFeature";
import { MetadataFeature } from "@/features/MetadataFeature";

/**
 * Registers all available project features with the global features catalog.
 */
export function registerProjectFeatures(): void {
    // When adding a new project feature, always register it here
    ProjectFeaturesCatalog.registerItem(MetadataFeature.FeatureID, new MetadataFeature());
    ProjectFeaturesCatalog.registerItem(DataManagementPlanFeature.FeatureID, new DataManagementPlanFeature());

    const names = Object.keys(ProjectFeaturesCatalog.items).map((item) => `${ProjectFeaturesCatalog.items[item].displayName} (${item})`);
    logging.debug(`-- Registered project features: ${names.join("; ")}`);
}
