import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { ResourcePreviewer } from "./ResourcePreviewer";

/**
 * Global catalog of all registered resource previewers.
 */
@ItemsCatalog.define()
export class ResourcePreviewersCatalog extends ItemsCatalog<ResourcePreviewer> {
    /**
     * Finds a previewer matching the specified MIME type.
     *
     * @param mimeType - The MIME type to find.
     *
     * @returns - The matching resource previewer, if any.
     */
    public static find(mimeType: string): ResourcePreviewer | undefined {
        return Object.values(this.items).find((previewer: ResourcePreviewer) => previewer.matches(mimeType));
    }
}
