import { SemVer } from "semver";

import { PropertySet } from "./PropertySet";
import { type PropertyProfile } from "./PropertyProfile";

export interface PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    getValue(ategory: string, id: string): any;
    setValue(category: string, id: string, value: any): void;
    propertiesToString(): string;
}

export class MetadataController implements PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    public constructor(profile: PropertyProfile, propertySet: PropertySet) {
        this.profile = profile;
        this.propertySet = propertySet;
    }

    public getValue(category: string, id: string): any {
        return this.propertySet.getProperty(category, id);
    }

    public setValue(category: string, id: string, value: any): void {
        this.propertySet.setProperty(category, id, value);
    }

    public propertiesToString(): string {
        return this.propertySet.toString();
    }
}
