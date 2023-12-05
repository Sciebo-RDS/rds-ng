import { ItemsCatalog } from "../utils/ItemsCatalog";
import { ProjectFeature, ProjectFeatureFlags } from "./ProjectFeature";

/**
 * Global catalog of all registered backend types.
 *
 * This is a globally accessible list of all project features, associated with their respective IDs.
 */
@ItemsCatalog.define()
export class ProjectFeaturesCatalog extends ItemsCatalog<ProjectFeature> {
    public static filter(flags: ProjectFeatureFlags): ProjectFeature[] {
        return Object.values(this.items).filter((feature) => feature.hasFlags(flags));
    }
}
