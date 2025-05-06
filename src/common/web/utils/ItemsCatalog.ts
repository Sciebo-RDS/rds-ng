import { type Constructable } from "./Types";

/**
 * Generic catalog to keep track of "registered" items (where the definition of "item" is completely context dependant).
 *
 * This is a globally accessible list of these items, associated with their respective names.
 */
export class ItemsCatalog<ItemType> {
    // @ts-ignore
    private static _items: Record<string, ItemType> = {};

    /**
     * A decorator to define a new item catalog.
     *
     * Notes:
     *     This decorator must always be used for new item catalogs; otherwise, data corruption might occur.
     */
    public static define(): Function {
        return (ctor: Constructable): Constructable => {
            return class extends ctor {
                // @ts-ignore
                private static _items: Record<string, ItemType> = {};
            };
        };
    }

    /**
     * Registers a new item.
     *
     * @param name - The item name.
     * @param item - The item.
     */
    // @ts-ignore
    public static registerItem(name: string, item: ItemType): void {
        if (name in this._items) {
            if (this._items[name] != item) {
                throw new Error(`An item with the name '${name}' has already been registered to a different item`);
            }
        } else {
            this._items[name] = item;
        }
    }

    /**
     * Finds the item associated with the given ``name``.
     *
     * @param name - The item name.
     *
     * @returns - The associated item, if any.
     */
    // @ts-ignore
    public static findItem(name: string): ItemType | undefined {
        return name in this._items ? this._items[name] : undefined;
    }

    /**
     * Retrieves all stored items.
     */
    // @ts-ignore
    public static get items(): Record<string, ItemType> {
        return this._items;
    }
}
