import { SemVer } from "semver";

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
    component: string;
    default?: boolean;
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
}

export const testProfile: PropertyProfile = {
    version: "1.1.1",
    name: "Test Profile",
    categories: [
        {
            id: "General",
            name: "General",
            properties: [
                {
                    id: "Author",
                    name: "Author",
                    type: PropertyDataType.STRING,
                    description: "The Authors name",
                    showAlways: true,
                    component: "something",
                    default: true,
                },
            ],
        },
        {
            id: "OSF",
            name: "OSF",
            properties: [
                {
                    id: "NumberOfAuthors",
                    name: "Number of Authors",
                    type: PropertyDataType.NUMBER,
                    description:
                        "This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! ",
                    showAlways: true,
                    component: "something",
                    default: true,
                },
                {
                    id: "SomeMultiselect",
                    name: "Some Multiselect",
                    type: PropertyDataType.MULTISELECT,
                    description: "Here are some options",
                    showAlways: false,
                    component: "something",
                    default: true,
                    options: ["asd", "something else", "another thing"],
                },
                {
                    id: "Number",
                    name: "Number",
                    type: PropertyDataType.NUMBER,
                    description: "The number of authors",
                    showAlways: false,
                    component: "something",
                    default: false,
                },
                {
                    id: "Authors",
                    name: "Authors",
                    type: PropertyDataType.TEXTAREA,
                    description: "The Authors name",
                    showAlways: false,
                    component: "something",
                },
            ],
        },
    ],
};

// TODO Make this Property type compatible with the Property type in PropertySet.ts
export const testValues = {
    profile_id: ["Test Profile", "1.1.1"],
    properties: {
        General: {
            Author: "John Doee",
        },
        OSF: {
            SomeMultiselect: ["asd", "another thing"],
        },
    },
};
