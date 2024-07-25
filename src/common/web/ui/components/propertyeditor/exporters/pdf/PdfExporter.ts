import { Exporter, type ExporterID } from "../Exporter";
import { PdfExporterExport } from "./_PdfExporter";
import { DmpDocumentDefinition } from "./DocumentDefinition";

export class PdfExporter extends Exporter {
    public static readonly ExporterID: ExporterID = "pdf";

    public constructor() {
        super(PdfExporter.ExporterID, {
            name: "PDF",
            Dmp: true,
            menuItem: {
                label: "PDF",
                icon: "pi pi-file-pdf",
                command: (controller, title) => {
                    main(controller, title);
                }
            }
        });
    }
}

function main(controller: any, title: string) {
    const profileIds = controller.getProfileIds();

    const documentDefinition = new DmpDocumentDefinition(controller, profileIds[0]);

    documentDefinition.title = title;
    //documentDefinition.logoImage =
    ("data:image/png;base64,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");
    documentDefinition.addCurrentDate();
    documentDefinition.addToc();

    for (const profileId of profileIds) {
        const categories = controller.getCategoryById(profileId);

        for (const category of categories) {
            documentDefinition.addCategory(category);
        }
    }

    const dD = documentDefinition.buildDocumentDefinition();
    PdfExporterExport.downloadPdf(dD, title);
}
