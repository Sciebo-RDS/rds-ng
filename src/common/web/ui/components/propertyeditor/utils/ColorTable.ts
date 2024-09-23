/**
 * Global color table based on item IDs.
 */
export class ColorTable {
    private static readonly _colorIDs: string[] = [];

    /**
     * Gets the color of a specific item.
     *
     * @param colorID - The item ID.
     * @param lightness - The color lightness.
     * @param amount - The color amount.
     * @param alpha - An optional alpha value.
     */
    public static color(colorID: string, lightness: number = 90, amount: number = 25, alpha: number = 1.0): string {
        if (!(colorID in ColorTable._colorIDs)) {
            ColorTable._colorIDs.push(colorID);
        }
        const index = ColorTable._colorIDs.indexOf(colorID);
        return `lch(${lightness} ${amount} ${(360.0 / Math.min(5, ColorTable._colorIDs.length)) * index} / ${alpha})`;
    }
}
