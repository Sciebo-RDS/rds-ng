import { type PropertyProfile, PropertyDataType } from "./PropertyProfile";

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
                },
                {
                    id: "SomeMultiselect",
                    name: "Some Multiselect",
                    type: PropertyDataType.MULTISELECT,
                    description: "Here are some options",
                    showAlways: false,
                    component: "something",
                    options: ["asd", "something else", "another thing"],
                },
                {
                    id: "Number",
                    name: "Number",
                    type: PropertyDataType.NUMBER,
                    description: "The number of authors",
                    showAlways: false,
                    component: "something",
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
