import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";
import { Exporter, type ExporterID } from "../Exporter";

export class RawExporter extends Exporter {
    public static readonly ExporterID: ExporterID = "raw";

    public constructor() {
        super(RawExporter.ExporterID, {
            name: "RAW",
            Dmp: true,
            menuItem: {
                label: "RAW",
                icon: "pi pi-code",
                command: (controller, title) => {
                    this._downloadRaw(controller, title);
                },
            },
        });
    }

    // https://www.raymondcamden.com/2020/12/15/vue-quick-shot-downloading-data-as-a-file
    private _downloadRaw(controller: PropertyController<any>, title: string) {
        const filename = `DMP_${title.replaceAll(" ", "_")}_${new Date().toLocaleDateString()}.json`;
        const text = JSON.stringify(controller.exportData());

        const element = document.createElement("a");
        element.setAttribute("href", "data:text/csv;charset=utf-8," + encodeURIComponent(text));
        element.setAttribute("download", filename);

        element.style.display = "none";
        document.body.appendChild(element);

        element.click();
        document.body.removeChild(element);
    }
}
