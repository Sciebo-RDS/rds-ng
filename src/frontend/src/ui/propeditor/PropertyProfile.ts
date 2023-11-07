import { SemVer } from "semver";

import StringForm from "@/ui/propeditor/propForms/StringForm.vue";
import NumberForm from "@/ui/propeditor/propForms/NumberForm.vue";
import TextAreaForm from "@/ui/propeditor/propForms/TextAreaForm.vue";
import MultiSelectForm from "@/ui/propeditor/propForms/MultiSelectForm.vue";
import StringListForm from "@/ui/propeditor/propForms/StringListForm.vue";

export type ProfileName = string;

export type PropertyProfile = {
    version: SemVer;
    name: ProfileName;
    categories: PropertyCategory[];
};

export type PropertyCategory = {
    id: string;
    name: string | null;
    properties: (Property | SelectionProperty)[];
};

export type Property = {
    id: string;
    name: string;
    type: PropertyDataType;
    description: string;
    showAlways: boolean;
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
}

export const propertyDataForms: { [key in PropertyDataType]?: typeof Vue } = {
    [PropertyDataType.STRING]: StringForm,
    [PropertyDataType.NUMBER]: NumberForm,
    [PropertyDataType.TEXTAREA]: TextAreaForm,
    [PropertyDataType.MULTISELECT]: MultiSelectForm,
    [PropertyDataType.STRINGLIST]: StringListForm,
};
