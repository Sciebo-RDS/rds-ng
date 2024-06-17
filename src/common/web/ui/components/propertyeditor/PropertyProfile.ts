import { type Component } from "vue";

import StringForm from "./propertyforms/StringForm.vue";
import NumberForm from "./propertyforms/NumberForm.vue";
import TextAreaForm from "./propertyforms/TextAreaForm.vue";
import MultiSelectForm from "./propertyforms/MultiSelectForm.vue";
import StringListForm from "./propertyforms/StringListForm.vue";
import RadioButtonForm from "./propertyforms/RadioButtonForm.vue";
import DateForm from "./propertyforms/DateForm.vue";
import DropDownForm from "./propertyforms/DropdownForm.vue";
import CheckBoxForm from "./propertyforms/CheckBoxForm.vue";

export type ProfileID = [string, string];

class ProfileMetadata {
    public constructor(
        public readonly id: ProfileID,
        public readonly name: string,
        public readonly description: string,
        public readonly version: string
    ) {}
}

// make inputs its own class, distinguish inputs that have options
export class ProfileClass {
    public constructor(
        public readonly id: string,
        public readonly label: string,
        public readonly description?: string,
        public readonly labelTemplate?: string,
        public readonly required?: boolean,
        public readonly multiple?: boolean,
        public readonly example?: string,
        public readonly type?: string[],
        public readonly input?: { id: string; label: string; type: string; description?: string; options?: string[] }[]
    ) {}
}

export class ProfileLayoutClass extends ProfileClass {}

export class Profile {
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
