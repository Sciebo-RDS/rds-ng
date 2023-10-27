import { SemVer } from "semver";

import { PropertySet } from "./PropertySet";
import { type PropertyProfile } from "./PropertyProfile";

export interface PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    getValue(): any;
    setValue(category: string, name: string, value: any): void;
}

export class MetadataController implements PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    public constructor(profile: PropertyProfile, propertySet: PropertySet) {
        this.profile = profile;
        this.propertySet = propertySet;
    }

    //TODO
    public getValue(): any {
        return null;
    }

    public setValue(category: string, name: string, value: any): void {
        this.propertySet.setProperty(category, name, value);
    }
}
