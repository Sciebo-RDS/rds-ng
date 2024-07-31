import { type VueComponent } from "@common/component/WebComponent";

import { ResourcePreviewer } from "@/ui/components/resource/ResourcePreviewer";
import { defineAsyncComponent } from "vue";

/**
 * A resource previewer for PDFs.
 */
export class PdfPreviewer extends ResourcePreviewer {
    public constructor() {
        super(["application/pdf"]);
    }

    public get component(): VueComponent {
        return defineAsyncComponent(() => import("./PdfPreviewer.vue"));
    }
}
