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

    public readonly context?: string;

    public constructor(id: ProfileID, displayLabel: string, description: string) {
        this.id = id;
        this.displayLabel = displayLabel;
        this.description = description;
    }
}

/**
 * Enum representing the types of hints that can be used for an input in the property editor.
 *
 * @enum {string}
 * @property {HintType.Text} Text - Represents a textual hint.
 * @property {HintType.Link} Link - Represents a hyperlink hint.
 */
export enum HintType {
    Text = "text",
    Link = "link"
}

/**
 * Represents an input for a profile class.
 */
export class ProfileClassInput {
    /**
     * Creates an instance of `ProfileClassInput`.
     * @param id - The ID of the input.
     * @param label - The label of the input.
     * @param type - The type of the input.
     * @param description - The description of the input.
     * @param example - An example of the input.
     * @param options - The options of the input.
     * @param required - Whether the input is required.
     * @param hints - Hints for certain inputs
     */

    public readonly id: string;
    public readonly label: string;
    public readonly type: string;
    public readonly description?: string;
    public readonly example?: string;
    public readonly options?: string[];
    public required?: boolean;
    public hints?: { [key: string]: { [key: string]: any } };

    public constructor(
        id: string,
        label: string,
        type: string,
        description?: string,
        example?: string,
        options: string[] = [],
        required?: boolean,
        hints?: { [key: string]: { [key: string]: string } }
    ) {
        this.id = id;
        this.label = label;
        this.type = type;
        this.description = description;
        this.example = example;
        this.options = options;
        this.required = required;
        this.hints = hints;
    }

    /**
     * Retrieves the unique identifier of the property input.
     *
     * @returns {string} The identifier of the property input.
     */
    public getId(): string {
        return this.id;
    }

    /**
     * Retrieves the description of the property input.
     *
     * @returns {string | undefined} The description of the property input.
     */
    public getDescription(): string | undefined {
        return this.description;
    }

    /**
     * Retrieves the example of the property input.
     *
     * @returns {string | undefined} The example of the property input.
     */
    public getExample(): string | undefined {
        return this.example;
    }

    /**
     * Retrieves the label of the property input.
     *
     * @returns {string} The label of the property input.
     */
    public getLabel(): string {
        return this.label;
    }

    /**
     * Retrieves the type of the property input.
     *
     * @returns {string} The type of the property input.
     */
    public getType(): string {
        return this.type;
    }

    /**
     * Retrieves the options of the input.
     *
     * @returns {string[] | undefined} The options of the property input.
     */
    public getOptions(): string[] {
        return this.options!;
    }

    /**
     * Determines whether hints exist for the given input key.
     *
     * @param input - The key to check for associated hints.
     * @returns `true` if hints exist for the specified input key; otherwise, `false`.
     */
    public hasHints(input: string): boolean {
        return !!this.hints?.[input];
    }

    /**
     * Retrieves a hint based on the provided input and hint type.
     *
     * @param input - The key used to look up the hint.
     * @param hintType - The specific type of hint to retrieve.
     * @returns An object representing the hint, or undefined if no hint is found.
     */
    public getHint(input: string, hintType: HintType): any {
        return this.hints?.[input]?.[hintType];
    }
}

export class ProfileClassRef {
    public readonly classId: string;
    public readonly required: Boolean;
    public readonly inline: Boolean;
    public readonly multiple: Boolean;

    public constructor(classId: string, required: Boolean = false, inline: Boolean = false, multiple: Boolean = true) {
        this.classId = classId;
        this.required = required;
        this.inline = inline;
        this.multiple = multiple;
    }

    /**
     * Retrieves the class type identifier.
     *
     * @returns {string} The class identifier.
     */
    public getClassId() {
        return this.classId;
    }

    /**
     * Checks if the ref property is set to inline mode.
     *
     * @returns {boolean} True if the property is inline, otherwise false.
     */
    public isInline() {
        return this.inline;
    }

    /**
     * Determines if multiple refs of this type are allowed.
     *
     * @returns {boolean} True if multiple refs are allowed, otherwise false.
     */
    public allowsMultiple() {
        return this.multiple;
    }
}

/**
 * Represents a profile with various properties and inputs.
 */
export class ProfileClass {
    public readonly id: string;
    public readonly displayLabel: string;
    public readonly description?: string;
    public readonly labelTemplate?: string;
    public required?: boolean;
    public readonly multiple?: boolean;
    public readonly example?: string;

    //@ts-ignore
    @Type(() => ProfileClassRef)
    public readonly refs: ProfileClassRef[];

    // @ts-ignore
    @Type(() => ProfileClassInput)
    public readonly input: ProfileClassInput[];

    public constructor(
        id: string,
        displayLabel: string,
        description?: string,
        labelTemplate?: string,
        required?: boolean,
        multiple?: boolean,
        example?: string,
        refs: ProfileClassRef[] = [],
        input: ProfileClassInput[] = []
    ) {
        this.id = id;
        this.displayLabel = displayLabel;
        this.description = description;
        this.labelTemplate = labelTemplate;
        this.required = required;
        this.multiple = multiple;
        this.example = example;
        this.refs = refs;
        this.input = input;
    }

    /**
     * Retrieves the inputs of the ProfileClass.
     *
     * @returns The input property.
     */
    public getInputs() {
        return this.input;
    }

    /**
     * Retrieves the types that the ProfileClass can reference.
     *
     * @returns The types of the ProfileClass.
     */
    public getRefTypes(): ProfileClassRef[] {
        return this.refs;
    }

    /**
     * Retrieves the unique identifier of the ProfileClass.
     *
     * @returns {string} The unique identifier of the ProfileClass.
     */
    public getId() {
        return this.id;
    }

    /**
     * Retrieves the displayLabel of the ProfileClass.
     *
     * @returns {string} The displayLabel of the ProfileClass.
     */
    public getDisplayLabel() {
        return this.displayLabel;
    }

    /**
     * Retrieves the description of the property class.
     *
     * @returns {string} The description of the property class.
     */
    public getDescription() {
        return this.description;
    }

    /**
     * Retrieves an example for the property class.
     *
     * @returns The current value of the example class.
     */
    public getExample() {
        return this.example;
    }

    /**
     * Checks if the property is required.
     *
     * @returns {boolean} True if the property is required, otherwise false.
     */
    public isRequired() {
        return this.required;
    }
}

/**
 * Represents a layout class for profiles, extending the ProfileClass.
 * This class maintains an array of profile IDs.
 */
export class ProfileLayoutClass extends ProfileClass {
    profiles: ProfileID[] = [];

    /**
     * Adds a profile to the profiles array of the ProfileLayoutClass.
     *
     * @param profile - The profile ID to be added.
     */
    addProfile(profile: ProfileID) {
        this.profiles!.push(profile);
    }

    /**
     * Retrieves the list of profiles.
     *
     * @returns {Profile[]} An array of profiles.
     */
    public getProfiles() {
        return this.profiles;
    }
}

/**
 * A dictionary that maps string keys to instances of `ProfileClass`.
 * This can be used to store and retrieve `ProfileClass` objects by their associated string identifiers.
 */
class ProfileClassDictionary {
    [key: string]: ProfileClass;
}

/**
 * Represents a property profile with metadata, layout, and classes.
 *
 * @remarks
 * This class is used to encapsulate the profile metadata, layout, and class dictionary
 * for a property editor component.
 *
 * @public
 */
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

    /**
     * Gets the layout part of the profile
     * @returns the profile layout
     */
    getLayout(): ProfileLayoutClass[] {
        return this.layout;
    }

    /**
     * Gets the classes part of the profile
     * @returns the profile classes
     */
    getClasses(): ProfileClassDictionary | undefined {
        return this.classes;
    }

    /**
     * Gets the version part of the ProfileID
     * @returns the ProfileID version
     */
    public getId(): ProfileID {
        return this.metadata.id;
    }

    /**
     * Gets the name part of the ProfileID
     * @returns the ProfileID name
     */
    getName(): string {
        return this.metadata.id[0];
    }

    /**
     * Gets the version part of the ProfileID
     * @returns the ProfileID version
     */
    getVersion(): string {
        return this.metadata.id[1];
    }

    /**
     * Retrieves the display label from the metadata.
     *
     * @returns {string} The display label.
     */
    getDisplayLabel(): string {
        return this.metadata.displayLabel;
    }
}

/**
 * Enum representing various property data types.
 *
 * @enum {string}
 * @property {string} STRING - Represents a string data type.
 * @property {string} NUMBER - Represents a number data type.
 * @property {string} BOOLEAN - Represents a boolean data type.
 * @property {string} SELECTION - Represents a selection data type.
 * @property {string} TEXTAREA - Represents a textarea data type.
 * @property {string} MULTISELECT - Represents a multiselect data type.
 * @property {string} STRINGLIST - Represents a string list data type.
 * @property {string} RADIOBUTTONS - Represents a radio buttons data type.
 * @property {string} DATE - Represents a date data type.
 * @property {string} DROPDOWN - Represents a dropdown data type.
 * @property {string} CHECKBOX - Represents a checkbox data type.
 */
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

/**
 * A mapping of `PropertyDataType` to their corresponding form components.
 * This object is used to dynamically render the appropriate form component
 * based on the type of property data.
 *
 * @typeParam PropertyDataType - The type of property data.
 * @typeParam Component - The form component associated with the property data type.
 *
 * @property {Component} [PropertyDataType.STRING] - Component for string data type.
 * @property {Component} [PropertyDataType.NUMBER] - Component for number data type.
 * @property {Component} [PropertyDataType.TEXTAREA] - Component for textarea data type.
 * @property {Component} [PropertyDataType.MULTISELECT] - Component for multiselect data type.
 * @property {Component} [PropertyDataType.STRINGLIST] - Component for string list data type.
 * @property {Component} [PropertyDataType.RADIOBUTTONS] - Component for radio buttons data type.
 * @property {Component} [PropertyDataType.DATE] - Component for date data type.
 * @property {Component} [PropertyDataType.DROPDOWN] - Component for dropdown data type.
 * @property {Component} [PropertyDataType.CHECKBOX] - Component for checkbox data type.
 */
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
