import { type VueComponent } from "@common/component/WebComponent";

import { ResourcePreviewer } from "@/ui/components/resource/ResourcePreviewer";
import { defineAsyncComponent } from "vue";

/**
 * A resource previewer for PDFs.
 */
export class TextPreviewer extends ResourcePreviewer {
    public constructor() {
        super(["text/plain", "text/html", "text/css", "text/csv", "*/json", "text/calendar", "*/javascript", "text/tab-separated-values", "*/xml"]);
    }

    public get component(): VueComponent {
        return defineAsyncComponent(() => import("./TextPreviewer.vue"));
    }
}
