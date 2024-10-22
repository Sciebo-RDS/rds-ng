import { Type } from "class-transformer";
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

    public readonly id: ProfileID;

    public readonly displayLabel: string;

    public readonly description: string;

    public constructor(id: ProfileID, displayLabel: string, description: string) {
        this.id = id;
        this.displayLabel = displayLabel;
        this.description = description;
    }
}

class ProfileClassInput {
    /**
     * Creates an instance of `ProfileClassInput`.
     * @param id - The ID of the input.
     * @param label - The label of the input.
     * @param type - The type of the input.
     * @param description - The description of the input.
     * @param example - An example of the input.
     * @param options - The options of the input.
     * @param required - Whether the input is required.
     */

    public readonly id: string;
    public readonly label: string;
    public readonly type: string;
    public readonly description?: string;
    public readonly example?: string;
    public readonly options?: string[];
    public required?: boolean;

    public constructor(id: string, label: string, type: string, description?: string, example?: string, options?: string[], required?: boolean) {
        this.id = id;
        this.label = label;
        this.type = type;
        this.description = description;
        this.example = example;
        this.options = options;
        this.required = required;
    }
}

// make inputs its own class, distinguish inputs that have options
export class ProfileClass {
    public readonly id: string;
    public readonly label: string;
    public readonly description?: string;
    public readonly labelTemplate?: string;
    public required?: boolean;
    public readonly multiple?: boolean;
    public readonly example?: string;
    public readonly type?: string[];

    // @ts-ignore
    @Type(() => ProfileClassInput)
    public readonly input?: ProfileClassInput[];

    public constructor(
        id: string,
        label: string,
        description?: string,
        labelTemplate?: string,
        required?: boolean,
        multiple?: boolean,
        example?: string,
        type?: string[],
        input?: ProfileClassInput[]
    ) {
        this.id = id;
        this.label = label;
        this.description = description;
        this.labelTemplate = labelTemplate;
        this.required = required;
        this.multiple = multiple;
        this.example = example;
        this.type = type;
        this.input = input;
    }
}

export class ProfileLayoutClass extends ProfileClass {
    profiles?: ProfileID[] = [];
}

class ProfileClassDictionary {
    [key: string]: ProfileClass;
}

export class PropertyProfile {
    // @ts-ignore
    @Type(() => ProfileMetadata)
    public readonly metadata: ProfileMetadata = new ProfileMetadata(["", ""], "", "");

    // @ts-ignore
    @Type(() => ProfileLayoutClass)
    public readonly layout: ProfileLayoutClass[] = [];

    // @ts-ignore
    @Type(() => ProfileClassDictionary)
    public readonly classes?: ProfileClassDictionary = {};

    public constructor(metadata: ProfileMetadata, layout: ProfileLayoutClass[], classes?: ProfileClassDictionary) {
        this.metadata = metadata;
        this.layout = layout;
        this.classes = classes;
    }
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
