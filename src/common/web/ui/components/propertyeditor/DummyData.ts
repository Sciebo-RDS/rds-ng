import { type PropertyProfile, PropertyDataType } from "./PropertyProfile";
import { type PersistedPropertySet } from "./PropertySet";

export const testProfile: PropertyProfile = {
    profile_id: { name: "Additional Profile", version: "1.1.1" },
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
                },
                {
                    id: "SomeMultiselect",
                    name: "Some Multiselect",
                    type: PropertyDataType.MULTISELECT,
                    description: "Here are some options",
                    showAlways: false,
                    options: ["asd", "something else", "another thing"],
                },
                {
                    id: "Radio",
                    name: "Some Radio Buttons",
                    type: PropertyDataType.RADIOBUTTONS,
                    description: "Here are some Radio Buttons",
                    showAlways: true,
                    options: ["asd", "something else", "another thing"],
                },
                {
                    id: "Radio",
                    name: "Some Radio Buttons",
                    type: PropertyDataType.RADIOBUTTONS,
                    description: "Here are some Radio Buttons",
                    showAlways: true,
                    options: ["asd", "something else", "another thing"],
                },
                {
                    id: "Number",
                    name: "Number",
                    type: PropertyDataType.NUMBER,
                    description: "The number of authors",
                    showAlways: false,
                },
                {
                    id: "Authors",
                    name: "Authors",
                    type: PropertyDataType.TEXTAREA,
                    description: "The Authors name",
                    showAlways: false,
                },
                {
                    id: "Authorslist",
                    name: "Authors list",
                    type: PropertyDataType.STRINGLIST,
                    description: "Comma separated list of authors",
                    showAlways: true,
                },
                {
                    id: "Publishdate",
                    name: "Publishing date",
                    type: PropertyDataType.DATE,
                    description: "When was this made publicly available?",
                    showAlways: true,
                },
            ],
        },
    ],
};

export const testValues: PersistedPropertySet = {
    profile_id: { name: "Additional Profile", version: "1.1.1" },
    properties: {
        General: {
            Author: "John Doee",
        },
        OSF: {
            SomeMultiselect: ["asd", "another thing"],
        },
    },
};
