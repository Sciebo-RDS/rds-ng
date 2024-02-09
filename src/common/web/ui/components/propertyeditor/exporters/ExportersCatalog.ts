import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { Exporter, type ExporterID } from "./Exporter";

/**
 * Global catalog of all registered exporters.
 *
 * This is a globally accessible list of all exporters, associated with their respective IDs.
 */
@ItemsCatalog.define()
export class ExportersCatalog extends ItemsCatalog<Exporter> {
    /**
     * Select certain exporters that satisfy the given predicate.
     *
     * @param predicate - The selection criterium.
     */
    public static filter(predicate: (exporter: Exporter) => boolean): Exporter[] {
        return Object.values(this.items).filter(predicate);
    }

    /**
     * Retrieve exporters by ID.
     */
    public static byID(id: ExporterID[]): Exporter[] {
        return id.map((id) => this.items[id]);
    }
}
