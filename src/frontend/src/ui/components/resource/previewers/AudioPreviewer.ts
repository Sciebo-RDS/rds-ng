import { type VueComponent } from "@common/component/WebComponent";

import { ResourcePreviewer } from "@/ui/components/resource/ResourcePreviewer";
import { defineAsyncComponent } from "vue";

/**
 * A resource previewer for images.
 */
export class AudioPreviewer extends ResourcePreviewer {
    public constructor() {
        super(["audio/*"]);
    }

    public get component(): VueComponent {
        return defineAsyncComponent(() => import("./AudioPreviewer.vue"));
    }
}
