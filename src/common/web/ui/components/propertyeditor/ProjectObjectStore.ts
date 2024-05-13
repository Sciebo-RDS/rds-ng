import { v4 as uuidv4 } from "uuid";

export class ProjectObject {
    id: string;
    profile: string;
    type: string;
    value: {};
    refs: string[];

    constructor(profile: string, type: string, id?: string, value?: any, refs?: string[]) {
        this.id = id || uuidv4();
        this.profile = profile;
        this.type = type;
        this.value = {};
        this.refs = refs || [];
    }
}

export class ProjectObjectStore {
    public _objects: ProjectObject[];

    constructor() {
        this._objects = [];
    }

    public add(object: ProjectObject): ProjectObject {
        const existing = this.get(object.id);
        if (existing) {
            return existing;
        }
        this._objects.push(object);
        return object;
    }

    public get(id: string): ProjectObject | undefined {
        return this._objects.find((object) => object.id === id);
    }

    public remove(id: string) {
        this._removeLinks(id);
        this._objects = this._objects.filter((object) => object.id !== id);
    }

    private _removeLinks(id: string) {
        this._objects.forEach((object) => {
            object.refs = object.refs.filter((ref) => ref !== id);
        });
    }

    public update(profileId: string, inputId: string, type: string, id: string, value: any) {
        const object = this.get(id) ? this.get(id) : this.add(new ProjectObject(profileId, type, id));
        if (object) {
            object["value"][inputId] = value;
        }
    }

    public addLink(id: string, ref: string) {
        const object = this.get(id);
        if (object) {
            object.refs.push(ref);
        } else console.log("object not found");
    }

    public removeLink(id: string, ref: string) {
        const object = this.get(id);
        if (object) {
            object.refs = object.refs.filter((r) => r !== ref);
        }
    }

    public getLinkedObjects(id: string): string[] {
        return this.get(id)["refs"] !== undefined ? this.get(id)["refs"] : [];
    }

    public getObjectsByType(type: string): ProjectObject[] {
        return this._objects.filter((object) => object.type === type);
    }
}
