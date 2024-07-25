import { ProjectObject } from "./ProjectObjectStore";

/**
 * Represents a history of navigated breadcrumb objects.
 */
export class History {
    _items: ProjectObject[] = [];

    constructor() {}

    /**
     * Navigates to the specified object and updates the history.
     * @param object - The object to navigate to.
     *
     * @returns The updated list of objects in the history.
     */
    public navigateTo(object: ProjectObject) {
        const pos = this._items.indexOf(this._items.filter((e) => e.id === object.id)[0]);
        if (pos != -1) {
            this._items = this._items.slice(0, pos + 1);
            return this._items;
        }

        this._addItem(object);
        return this.list();
    }

    /**
     * Returns the list of objects in the history.
     * @returns The list of objects in the history.
     */
    public list(): ProjectObject[] {
        return this._items;
    }

    private _addItem(object: ProjectObject) {
        this._items.push(object);
        return object;
    }
}
