import { type Component } from "vue";

import CheckBoxForm from "./propertyforms/CheckBoxForm.vue";
import DateForm from "./propertyforms/DateForm.vue";
import DropDownForm from "./propertyforms/DropdownForm.vue";
import MultiSelectForm from "./propertyforms/MultiSelectForm.vue";
import NumberForm from "./propertyforms/NumberForm.vue";
import RadioButtonForm from "./propertyforms/RadioButtonForm.vue";
import StringForm from "./propertyforms/StringForm.vue";
import StringListForm from "./propertyforms/StringListForm.vue";
import TextAreaForm from "./propertyforms/TextAreaForm.vue";

/**
 * Represents a profile ID. usually [profilename, profileversion]
 * @typedef {Array<string, string>} ProfileID
 */
export type ProfileID = [string, string];

/**
 * Represents the metadata of a profile.
 */
class ProfileMetadata {
    /**
     * Creates an instance of `ProfileMetadata`.
     * @param id - The ID of the profile.
     * @param displayLabel - The name of the profile.
     * @param description - The description of the profile.
     */
    public constructor(
        public readonly id: ProfileID,
        public readonly displayLabel: string,
        public readonly description: string
    ) {}
}

// make inputs its own class, distinguish inputs that have options
export class ProfileClass {
    public constructor(
        public readonly id: string,
        public readonly label: string,
        public readonly description?: string,
        public readonly labelTemplate?: string,
        public required?: boolean,
        public readonly multiple?: boolean,
        public readonly example?: string,
        public readonly type?: string[],
        public readonly input?: { id: string; label: string; type: string; description?: string; example?: string; options?: string[]; required?: boolean }[]
    ) {}
}

export class ProfileLayoutClass extends ProfileClass {
    profiles?: ProfileID[] = [];
}

export class PropertyProfile {
    public constructor(
        public readonly metadata: ProfileMetadata,
        public readonly layout: ProfileLayoutClass[],
        public readonly classes?: { [key: string]: ProfileClass }
    ) {}
}

export enum PropertyDataType {
    STRING = "string",
    NUMBER = "number",
    BOOLEAN = "boolean",
    SELECTION = "selection",
    TEXTAREA = "textarea",
    MULTISELECT = "multiselect",
    STRINGLIST = "stringlist",
    RADIOBUTTONS = "radiobuttons",
    DATE = "date",
    DROPDOWN = "dropdown",
    CHECKBOX = "checkbox"
}

export const propertyDataForms: { [key in PropertyDataType]?: Component } = {
    [PropertyDataType.STRING]: StringForm,
    [PropertyDataType.NUMBER]: NumberForm,
    [PropertyDataType.TEXTAREA]: TextAreaForm,
    [PropertyDataType.MULTISELECT]: MultiSelectForm,
    [PropertyDataType.STRINGLIST]: StringListForm,
    [PropertyDataType.RADIOBUTTONS]: RadioButtonForm,
    [PropertyDataType.DATE]: DateForm,
    [PropertyDataType.DROPDOWN]: DropDownForm,
    [PropertyDataType.CHECKBOX]: CheckBoxForm
};
