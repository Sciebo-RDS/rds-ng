import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { SnapIn } from "./SnapIn";

/**
 * Global catalog of all registered snap-ins.
 *
 * This is a globally accessible list of all snap-ins, associated with their respective IDs.
 */
@ItemsCatalog.define()
export class SnapInsCatalog extends ItemsCatalog<SnapIn> {
    /**
     * Select certain snap-ins that satisfy the given predicate.
     *
     * @param predicate - The selection criterium.
     */
    public static filter(predicate: (snapIn: SnapIn) => boolean): SnapIn[] {
        return Object.values(this.items).filter(predicate);
    }

    /**
     * Retrieve all optional snap-ins.
     */
    public static allOptionals(): SnapIn[] {
        return this.filter((snapIn) => snapIn.isOptional());
    }

    /**
     * Retrieve all snap-ins with a tab panel.
     */
    public static allWithTabPanel(): SnapIn[] {
        return this.filter((snapIn) => snapIn.hasTabPanel());
    }
}
