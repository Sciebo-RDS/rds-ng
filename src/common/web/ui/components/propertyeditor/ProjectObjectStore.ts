// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import { type ProfileID } from "./PropertyProfile";

export class ProjectObject {
    id: string;
    profile: ProfileID;
    value: { [key: string]: any };
    refs: string[];
    type?: string;

    constructor(profile: ProfileID, type: string | null, id?: string, value: any = {}, refs: string[] = []) {
        this.id = id || uuidv4();
        this.profile = profile;
        if (type !== null) this.type = type;
        this.value = value;
        this.refs = refs;
    }
}

export class ProjectObjectStore {
    public _objects: ProjectObject[];

    constructor() {
        this._objects = [];
    }

    public setObjects(objects: ProjectObject[]) {
        this._objects = objects;
    }

    public exportObjects(): ProjectObject[] {
        return this._objects;
    }

    public add(object: ProjectObject): ProjectObject {
        const existing = this.get(object.id);
        if (existing !== undefined) {
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

    public _removeLinks(id: string) {
        this._objects.forEach((object) => {
            object.refs = object.refs.filter((ref) => ref !== id);
        });
    }

    public update(profileId: ProfileID, inputId: string, id: string, value: any) {
        const object: ProjectObject = this.add(new ProjectObject(profileId, null, id)) as ProjectObject;
        if (object !== undefined) {
            object["value"][inputId] = value;
        }
    }

    public addLink(id: string, ref: string) {
        const object = this.get(id);
        if (object) {
            object.refs.push(ref);
        } else return undefined;
    }

    public removeLink(id: string, ref: string) {
        const object = this.get(id);
        if (object) {
            object.refs = object.refs.filter((r) => r !== ref);
        }
    }

    public getLinkedObjects(id: string): string[] {
        const object = this.get(id);
        return object ? object["refs"] : [];
    }

    public getObjectsByType(type: string): ProjectObject[] {
        return this._objects.filter((object) => object.type === type);
    }
}
