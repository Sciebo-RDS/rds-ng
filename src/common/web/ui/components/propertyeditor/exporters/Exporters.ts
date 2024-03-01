import { type Constructable } from "../../../../utils/Types";

import { Exporter, type ExporterID } from "./Exporter";
import { ExportersCatalog } from "./ExportersCatalog";

import { PdfExporter } from "./pdf/PdfExporter";
import { RawExporter } from "./raw/RawExporter";

/**
 * Registers all available exporters.
 *
 * When adding a new snap-in, always register it here.
 */
export function registerExporters(): void {
    interface ConstructableExporter extends Constructable<Exporter> {
        ExporterID: ExporterID;
    }

    function registerExporter(exporter: ConstructableExporter): void {
        ExportersCatalog.registerItem(exporter.ExporterID, new exporter());
    }

    // New exporters go here; the order in which they are added also define the order of their MenuItems

    registerExporter(PdfExporter);
    registerExporter(RawExporter);
}
