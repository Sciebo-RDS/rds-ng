import { plainToInstance } from "class-transformer";
import { Profile, ProfileClass, type ProfileID } from "./PropertyProfile";

const isProfile = (profile: any): profile is Profile => {
    return (
        profile.metadata &&
        profile.metadata.id &&
        profile.metadata.version &&
        profile.layout &&
        profile.metadata.name &&
        profile.layout.length > 0 &&
        profile.metadata.id.length == 2
    );
};

export class PropertyProfileStore {
    private _profiles: Profile[];

    constructor() {
        this._profiles = [];
    }

    public mountProfile(profile: Profile) {
        try {
            if (isProfile(profile)) {
                this._profiles.push(plainToInstance(Profile, profile) as Profile);
                console.log("mounted profile: ", profile);
            } else {
                console.log("Invalid profile: ", profile);
            }
        } catch (e) {
            console.log("Error mounting profile");
        }
    }

    public unmountProfile(profileId: ProfileID) {
        this._profiles = this._profiles.filter((profile) => profile.metadata.id !== profileId);
    }

    public getClassById(classId: string): ProfileClass | undefined {
        let classes = {} as { [key: string]: ProfileClass };
        this._profiles.forEach((profile) => (classes = { ...classes, ...profile.classes }));
        return classes[classId];
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
