import { Profile, ProfileClass, type ProfileID } from "./PropertyProfile";

export class PropertyProfileStore {
    private _profiles: Profile[];

    constructor() {
        this._profiles = [];
    }

    public mountProfile(profile: Profile) {
        this._profiles.push(profile);
    }

    public unmountProfile(profileId: ProfileID) {
        this._profiles = this._profiles.filter((profile) => profile.metadata.id !== profileId);
    }

    public getClassById(profileId: ProfileID, classId: string): ProfileClass | undefined {
        const profile = this._profiles.find((profile) => profile.metadata.id === profileId);
        return profile?.classes ? profile.classes[classId] : undefined;
    }

    public list(): Profile[] {
        return this._profiles;
    }

    public listClasses(): ProfileClass[] {
        return this._profiles.flatMap((profile) => (!!profile.classes ? Object.values(profile.classes) : []));
    }
}
