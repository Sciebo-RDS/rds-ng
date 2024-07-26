import { type VueComponent } from "@common/component/WebComponent";

import { ResourcePreviewer } from "@/ui/components/resource/ResourcePreviewer";
import { defineAsyncComponent } from "vue";

/**
 * A resource previewer for PDFs.
 */
export class TextPreviewer extends ResourcePreviewer {
    public constructor() {
        super("text/*");
    }

    public get component(): VueComponent {
        return defineAsyncComponent(() => import("./TextPreviewer.vue"));
    }
}
