import { v4 as uuidv4 } from "uuid";
import { Profile, ProfileClass } from "./PropertyProfile";

export class PropertyProfileStore {
    private _profiles: Profile[];

    constructor() {
        this._profiles = [];
    }

    public mountProfile(profile: Profile) {
        this._profiles.push(profile);
    }

    public unmountProfile(profileId: string) {
        this._profiles = this._profiles.filter((profile) => profile.metadata.id !== profileId);
    }

    public getClassById(profileId: string, classId: string): ProfileClass | undefined {
        const profile = this._profiles.find((profile) => profile.metadata.id === profileId);
        return profile ? profile.classes[classId] : undefined;
    }

    public list(): Profile[] {
        return this._profiles;
    }
}
