import { SemVer } from "semver";

export type ProfileName = string;

export type PropertyProfile = {
    version: SemVer;
    name: ProfileName;
    categories: PropertyCategory[];
};

//categories should rather be subprofiles?
export type PropertyCategory = {
    name: string | null;
    properties: (Property | SelectionProperty)[];
};

export type Property = {
    name: string;
    type: PropertyDataType;
    description: string;
    required: boolean;
    component: string;
    default?: boolean;
    filter?: string[];
};

export type SelectionProperty = Property & {
    options: string[];
};

export type PropertyDataType =
    | "string"
    | "number"
    | "boolean"
    | "selection"
    | "textarea"
    | "multiselect";

export const testProfile: PropertyProfile = {
    version: "1.1.1",
    name: "Test Profile",
    categories: [
        {
            name: "General",
            properties: [
                {
                    name: "Author",
                    type: "string",
                    description: "The Authors name",
                    required: true,
                    component: "something",
                    default: true,
                },
            ],
        },
        {
            name: "OSF",
            properties: [
                {
                    name: "Number of Authors",
                    type: "number",
                    description:
                        "This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! ",
                    required: false,
                    component: "something",
                    default: true,
                },
                {
                    name: "Some Multiselect",
                    type: "multiselect",
                    description: "Here are some options",
                    required: false,
                    component: "something",
                    default: true,
                    options: ["asd", "something else", "another thing"],
                },
                {
                    name: "Number",
                    type: "number",
                    description: "The number of authors",
                    required: false,
                    component: "something",
                    default: false,
                },
                {
                    name: "Authors",
                    type: "textarea",
                    description: "The Authors name",
                    required: true,
                    component: "something",
                },
            ],
        },
    ],
};

export const testValues = {
    profile_id: ["Test Profile", "1.1.1"],
    properties: {
        General: {
            Author: "John Doee",
        },
        OSF: {
            "Number of Authors": 2,
            "Some Multiselect": ["asd", "another thing"],
            Authors: "John Doe, Jane Doe, someone",
        },
    },
};
