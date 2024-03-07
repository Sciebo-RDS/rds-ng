import type { Component } from "vue";

import StringForm from "./propertyforms/StringForm.vue";
import NumberForm from "./propertyforms/NumberForm.vue";
import TextAreaForm from "./propertyforms/TextAreaForm.vue";
import MultiSelectForm from "./propertyforms/MultiSelectForm.vue";
import StringListForm from "./propertyforms/StringListForm.vue";
import RadioButtonForm from "./propertyforms/RadioButtonForm.vue";
import DateForm from "./propertyforms/DateForm.vue";
import DropDownForm from "./propertyforms/DropdownForm.vue";
import CheckBoxForm from "./propertyforms/CheckBoxForm.vue";

export class ProfileID {
    public constructor(
        public readonly name: string,
        public readonly version: string
    ) {}
}

export type PropertyProfile = {
    profile_id: ProfileID;
    categories: PropertyCategory[];
};

export type PropertyCategory = {
    id: string;
    name: string;
    description?: string;
    properties: (Property | SelectionProperty)[];
};

export type Property = {
    id: string;
    name: string;
    type: PropertyDataType;
    description: string;
    required?: boolean;
    showAlways?: boolean;
    filter?: string[];
};

export type SelectionProperty = Property & {
    options: string[];
};

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
    CHECKBOX = "checkbox",
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
    [PropertyDataType.CHECKBOX]: CheckBoxForm,
};
