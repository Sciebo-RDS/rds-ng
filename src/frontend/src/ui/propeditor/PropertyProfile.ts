import { SemVer } from "semver";

import StringForm from "@/ui/propeditor/propForms/StringForm.vue";
import NumberForm from "@/ui/propeditor/propForms/NumberForm.vue";
import TextAreaForm from "@/ui/propeditor/propForms/TextAreaForm.vue";
import MultiSelectForm from "@/ui/propeditor/propForms/MultiSelectForm.vue";
import StringListForm from "@/ui/propeditor/propForms/StringListForm.vue";
import RadioButtonForm from "@/ui/propeditor/propForms/RadioButtonForm.vue";
import DateForm from "@/ui/propeditor/propForms/DateForm.vue";
import DropDownForm from "@/ui/propeditor/propForms/DropdownForm.vue";
import CheckBoxForm from "@/ui/propeditor/propForms/CheckBoxForm.vue";

export type ProfileID = { name: string; version: SemVer };

export type PropertyProfile = {
    profile_id: ProfileID;
    categories: PropertyCategory[];
};

export type PropertyCategory = {
    id: string;
    name?: string;
    description?: string;
    properties: (Property | SelectionProperty)[];
};

export type Property = {
    id: string;
    name: string;
    type: PropertyDataType;
    description: string;
    required?: boolean;
    showAlways: boolean;
    filter?: string[];
};

type SelectionProperty = Property & {
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

export const propertyDataForms: { [key in PropertyDataType]?: typeof Vue } = {
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
