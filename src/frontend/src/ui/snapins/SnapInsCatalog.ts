import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { SnapIn, SnapInFlags } from "./SnapIn";

/**
 * Global catalog of all registered snap-ins.
 *
 * This is a globally accessible list of all snap-ins, associated with their respective IDs.
 */
@ItemsCatalog.define()
export class SnapInsCatalog extends ItemsCatalog<SnapIn> {
    public static filter(flags: SnapInFlags): SnapIn[] {
        return Object.values(this.items).filter((feature) => feature.hasFlags(flags));
    }
}
