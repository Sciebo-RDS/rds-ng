import { ProjectObject } from "./ProjectObjectStore";

export class History {
    _items: ProjectObject[] = [];

    constructor() {}

    public navigateTo(object: ProjectObject) {
        const pos = this._items.indexOf(this._items.filter((e) => e.id === object.id)[0]);
        if (pos != -1) {
            this._items = this._items.slice(0, pos + 1);
            return this._items;
        }

        this._addItem(object);
        return this.list();
    }

    public list(): ProjectObject[] {
        return this._items;
    }

    private _addItem(object: ProjectObject) {
        this._items.push(object);
        return object;
    }
}
