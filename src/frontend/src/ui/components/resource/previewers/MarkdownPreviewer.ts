import { type VueComponent } from "@common/component/WebComponent";

import { ResourcePreviewer } from "@/ui/components/resource/ResourcePreviewer";
import { defineAsyncComponent } from "vue";

/**
 * A resource previewer for Markdown files.
 */
export class MarkdownPreviewer extends ResourcePreviewer {
    public constructor() {
        super(["text/markdown"]);
    }

    public get component(): VueComponent {
        return defineAsyncComponent(() => import("./MarkdownPreviewer.vue"));
    }
}
