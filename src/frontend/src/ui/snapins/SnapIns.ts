import logging from "@common/core/logging/Logging";
import { type SnapInID } from "@common/data/entities/EntityTypes";
import { type Constructable } from "@common/utils/Types";

import { SnapIn } from "./SnapIn";
import { SnapInsCatalog } from "./SnapInsCatalog";

import { DataManagementPlanSnapIn } from "./dmp/DataManagementPlanSnapIn";
import { MetadataSnapIn } from "./metadata/MetadataSnapIn";
import { SummarySnapIn } from "./summary/SummarySnapIn";

/**
 * Registers all available snap-ins.
 *
 * When adding a new snap-in, always register it here.
 */
export function registerSnapIns(): void {
    interface ConstructableSnapIn extends Constructable<SnapIn> {
        SnapInID: SnapInID;
    }

    function registerSnapIn(snapIn: ConstructableSnapIn): void {
        SnapInsCatalog.registerItem(snapIn.SnapInID, new snapIn());
    }

    // New snap-ins go here; the order in which they are added also define the order of their panels
    registerSnapIn(MetadataSnapIn);
    registerSnapIn(DataManagementPlanSnapIn);
    registerSnapIn(SummarySnapIn);

    // Print all available snap-ins for debugging purposes
    const names = Object.keys(SnapInsCatalog.items).map((item) => `${SnapInsCatalog.items[item].displayName} (${item})`);
    logging.debug(`Registered snap-ins: ${names.join("; ")}`);
}
