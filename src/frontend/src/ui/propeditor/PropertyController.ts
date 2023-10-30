import { SemVer } from "semver";

import { PropertySet } from "./PropertySet";
import { type PropertyProfile } from "./PropertyProfile";

export interface PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    getValue(ategory: string, name: string): any;
    setValue(category: string, name: string, value: any): void;
    propertiesToString(): string;
}

export class MetadataController implements PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    public constructor(profile: PropertyProfile, propertySet: PropertySet) {
        this.profile = profile;
        this.propertySet = propertySet;
    }

    public getValue(category: string, name: string): any {
        return this.propertySet.getProperty(category, name);
    }

    public setValue(category: string, name: string, value: any): void {
        this.propertySet.setProperty(category, name, value);
    }

    public propertiesToString(): string {
        return JSON.stringify(this.propertySet);
    }
}
