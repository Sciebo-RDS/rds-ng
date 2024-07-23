// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import { type ProfileID } from "./PropertyProfile";

/**
 * Represents a project object.
 */
export abstract class ProjectObject {
    id: string;
    value: { [key: string]: any };
    refs: string[];

    /**
     * Creates a new instance of ProjectObject.
     * @param id The object ID.
     * @param value The object value.
     * @param refs The object references.
     */
    constructor(id?: string, value: any = {}, refs: string[] = []) {
        this.id = id || uuidv4();
        this.value = value;
        this.refs = refs;
    }
}

export class LayoutObject extends ProjectObject {
    profiles: ProfileID[];

    constructor(profiles: ProfileID[], id?: string, value: any = {}, refs: string[] = []) {
        super(id, value, refs);
        this.profiles = profiles;
    }
}

export class SharedObject extends ProjectObject {
    type: string;

    constructor(type: string, id?: string, value: any = {}, refs: string[] = []) {
        super(id, value, refs);
        this.type = type;
    }
}

/**
 * Creates a dummy project object.
 *
 * @param id - The ID of the project object.
 * @returns A new instance of the ProjectObject class.
 */
export const dummyProjectObject = (id: string) => new SharedObject("dummy", id, {}, []);

/**
 * Represents a store for project objects.
 */
export class ProjectObjectStore {
    public _objects: ProjectObject[];

    /**
     * Constructs a new ProjectObjectStore instance.
     */
    constructor() {
        this._objects = [];
    }

    /**
     * Sets the objects in the store.
     * @param objects - An array of project objects.
     */
    public setObjects(objects: ProjectObject[]): void {
        this._objects = objects;
    }

    /**
     * Exports the objects from the store.
     * @returns An array of project objects.
     */
    public exportObjects(): ProjectObject[] {
        return this._objects;
    }

    /**
     * Adds a project object to the store if no object with that ID exists.
     * @param object - The project object to add.
     *
     * @returns The project object with that ID, either existing or newly created.
     */
    public add(object: ProjectObject): ProjectObject {
        const existing = this.get(object.id);
        if (existing !== undefined) {
            return existing;
        }
        this._objects.push(object);
        return object;
    }

    /**
     * Retrieves a project object by its ID.
     * @param id - The ID of the project object.
     *
     * @returns The project object with the specified ID, or undefined if not found.
     */
    public get(id: string): ProjectObject | undefined {
        return this._objects.find((object) => object.id === id);
    }

    /**
     * Removes a project object from the store by its ID. Also removes all references to the object.
     * @param id - The ID of the project object to remove.
     */
    public remove(id: string): void {
        this._removeRefs(id);
        this._objects = this._objects.filter((object) => object.id !== id);
    }

    /**
     * Removes references to a project object by its ID.
     * @param id - The ID of the project object.
     */
    public _removeRefs(id: string): void {
        this._objects.forEach((object) => {
            object.refs = object.refs.filter((ref) => ref !== id);
        });
    }

    /**
     * Updates the value of a project object.
     * @param profileId - The profile ID of the project object (only for LayoutObjects).
     * @param inputId - The input ID of the project object.
     * @param id - The ID of the project object.
     * @param value - The new value for the project object.
     */
    public update(profileId: ProfileID[] = [], inputId: string, id: string, value: any): void {
        var object: ProjectObject;

        if (profileId.length > 0) {
            object = this.add(new LayoutObject(profileId, id)) as LayoutObject;
        } else {
            object = this.get(id)!;
        }
        if (object !== undefined) {
            object["value"][inputId] = value;
        }
    }

    /**
     * Adds a reference to a project object.
     * @param id - The ID of the project object.
     * @param ref - The reference ID to add.
     *
     * @returns The updated project object, or undefined if the project object is not found.
     */
    public addRef(id: string, ref: string): ProjectObject | undefined {
        const object = this.get(id);
        if (object) {
            object.refs.push(ref);
        } else {
            return undefined;
        }
    }

    /**
     * Removes a reference from a project object.
     * @param id - The ID of the project object.
     * @param ref - The reference ID to remove.
     */
    public removeRef(id: string, ref: string): void {
        const object = this.get(id);
        if (object) {
            object.refs = object.refs.filter((r) => r !== ref);
        }
    }

    /**
     * Retrieves the referenced objects of a project object.
     * @param id - The ID of the project object.
     *
     * @returns An array of reference IDs of the referenced objects.
     */
    public getReferencedObjects(id: string): string[] {
        const object = this.get(id);
        return object ? object["refs"] : [];
    }

    /**
     * Retrieves project objects of a specific type.
     * @param type - The type of project objects to retrieve.
     *
     * @returns An array of project objects of the specified type.
     */
    public getObjectsByType(type: string): SharedObject[] {
        return this._objects.filter((obj) => !!obj.type && obj.type === type);
    }
}
