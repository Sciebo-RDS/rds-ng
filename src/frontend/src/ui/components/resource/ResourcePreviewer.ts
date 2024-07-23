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
    private readonly _mimeType: string;

    /**
     * @param mimeType - The MIME type; wildcards are supported.
     */
    protected constructor(mimeType: string) {
        this._mimeType = mimeType;
    }

    /**
     * Checks if the MIME type matches the type of this previewer.
     *
     * @param mimeType - The MIME type to check.
     */
    public matches(mimeType: string): boolean {
        let matcher = wildcardMatch(this._mimeType);
        return matcher(mimeType);
    }

    /**
     * The MIME type.
     */
    public get mimeType(): string {
        return this._mimeType;
    }

    /**
     * Gets the dynamic component for this previewer.
     */
    public abstract get component(): VueComponent;
}
