import { SemVer } from "semver";

import { Configuration } from "../utils/config/Configuration";
import { UnitID } from "../utils/UnitID";

/**
 * Holds general data and information about the component.
 *
 * Objects of this class are passed to certain parts of the core for easy access to frequently
 * used component information and data.
 */
export class ComponentData {
    /**
     * @param compID - The component identifier.
     * @param config - The configuration.
     * @param title - The project title.
     * @param name - The component name.
     * @param version - The project version.
     */
    public constructor(readonly compID: UnitID, readonly config: Configuration,
                       readonly title: string, readonly name: string, readonly version: SemVer) {
    }
}
