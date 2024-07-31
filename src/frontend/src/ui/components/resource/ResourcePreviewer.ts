// @ts-ignore
import wildcardMatch from "wildcard-match";

import { type VueComponent } from "@common/component/WebComponent";

/**
 * Dynamic preview Vue component loader.
 */
export type ResourcePreviewComponentLoader = () => any;

/**
 * A resource previewer encapsulates a preview component for specific MIME types.
 */
export abstract class ResourcePreviewer {
    private readonly _mimeTypes: string[];

    /**
     * @param mimeTypes - List of MIME types; wildcards are supported.
     */
    protected constructor(mimeTypes: string[]) {
        this._mimeTypes = mimeTypes;
    }

    /**
     * Checks if the MIME type matches the types supported by this previewer.
     *
     * @param mimeType - The MIME type to check.
     */
    public matches(mimeType: string): boolean {
        for (const mt of this._mimeTypes) {
            let matcher = wildcardMatch(mt);
            if (matcher(mimeType)) {
                return true;
            }
        }
        return false;
    }

    /**
     * The MIME types.
     */
    public get mimeTypes(): string[] {
        return this._mimeTypes;
    }

    /**
     * Gets the dynamic component for this previewer.
     */
    public abstract get component(): VueComponent;
}
