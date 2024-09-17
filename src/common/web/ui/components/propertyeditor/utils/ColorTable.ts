/**
 * Global color table based on item IDs.
 */
export class ColorTable {
    private static readonly _colorIDs: string[] = [];

    /**
     * Gets the color of a specific item.
     *
     * @param colorID - The item ID.
     * @param alpha - An optional alpha value.
     */
    public static color(colorID: string, alpha: number = 1.0): string {
        if (!(colorID in ColorTable._colorIDs)) {
            ColorTable._colorIDs.push(colorID);
        }
        const index = ColorTable._colorIDs.indexOf(colorID);
        return `lch(90 25 ${(360.0 / Math.min(5, ColorTable._colorIDs.length)) * index} / ${alpha})`;
    }
}
