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

    public getLabelTemplateById(classId: string): string | undefined {
        const profile = this._profiles.find((profile) => !!profile.classes && !!profile.classes[classId]);
        return profile?.classes![classId]["labelTemplate"];
    }

    public getClassLabelById(classId: string): string | undefined {
        const profile = this._profiles.find((profile) => !!profile.classes && !!profile.classes[classId]);
        return profile?.classes![classId]["label"];
    }

    public getProfileLabelById(profileId: ProfileID): string | undefined {
        const profile = this._profiles.find((profile) => profile.metadata.id === profileId);
        return profile?.metadata.name;
    }

    public list(): Profile[] {
        return this._profiles;
    }

    public listClasses(): ProfileClass[] {
        return this._profiles.flatMap((profile) => (!!profile.classes ? Object.values(profile.classes) : []));
    }
}
