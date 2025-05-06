import { type VueComponent } from "@common/component/WebComponent";

import { ResourcePreviewer } from "@/ui/components/resource/ResourcePreviewer";
import { defineAsyncComponent } from "vue";

/**
 * A resource previewer for images.
 */
export class ImagePreviewer extends ResourcePreviewer {
    public constructor() {
        super(["image/*"]);
    }

    public get component(): VueComponent {
        return defineAsyncComponent(() => import("./ImagePreviewer.vue"));
    }
}
