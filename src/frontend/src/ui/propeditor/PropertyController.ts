import { SemVer } from "semver";

import { PropertySet } from "./PropertySet";
import { type PropertyProfile } from "./PropertyProfile";

export interface PropertyController {
    profile: PropertyProfile;
    propertySet: PropertySet;

    getValue(ategory: string, id: string): any;
    setValue(
        debounce: number | null,
        category: string,
        id: string,
        value: any
    ): void;
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

    public setValue(
        debounce: number | null,
        category: string,
        id: string,
        value: any
    ): number {
        if (debounce) {
            clearTimeout(debounce);
        }

        return setTimeout(() => {
            this.propertySet.setProperty(category, id, value);
        }, 500);
    }

    public propertiesToString(): string {
        return this.propertySet.toString();
    }
}
