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

export const dataCite: PropertyProfile = {
    version: "4.4",
    name: "DataCite",
    categories: [
        {
            id: "Mandatory",
            name: "Mandatory",
            description: "Mandatory DataCite properties",
            properties: [
                {
                    id: "1",
                    name: "Identifier (DOI)",
                    type: PropertyDataType.STRING,
                    description:
                        "The Identifier is a unique string that identifies a resource. For software, determine whether the identifier is for a specific version of a piece of software, (per the Force11 Software Citation Principles or for all versions.",
                    showAlways: true,
                    required: true,
                },
                {
                    id: "2",
                    name: "Creator",
                    type: PropertyDataType.STRINGLIST,
                    description:
                        "The main researchers involved in producing the data, or the authors of the publication, in priority order. To supply multiple creators, repeat this property.",
                    showAlways: true,
                    required: true,
                },
                {
                    id: "3",
                    name: "Title",
                    type: PropertyDataType.STRING,
                    description:
                        "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software",
                    showAlways: true,
                    required: true,
                },
                {
                    id: "4",
                    name: "Publisher",
                    type: PropertyDataType.STRING,
                    description:
                        'The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role. For software, use Publisher for the code repository. If there is an entity other than a code repository, that "holds, archives, publishes, prints, distributes, releases, issues, or produces "the code, use the property Contributor/contributorType/ hostingInstitution for the code repository.',
                    showAlways: true,
                    required: true,
                },
                {
                    id: "5",
                    name: "Publication Year",
                    type: PropertyDataType.DATE,
                    description:
                        "The year when the data was or will be made publicly available. In the case of resources such as software or dynamic data where there may be multiple releases in one year, include the Date/dateType/ dateInformation property and sub-properties to provide more information about the publication or release date details",
                    showAlways: true,
                    required: true,
                },
                {
                    id: "10",
                    name: "Ressource Type",
                    type: PropertyDataType.STRING,
                    description:
                        " A description of the resource. The recommended content is a single term.",
                    showAlways: true,
                    required: true,
                },
            ],
        },
        {
            id: "Recommended",
            name: "Recommended",
            description: "Properties recommended by DataCite",
            properties: [
                {
                    id: "6",
                    name: "Subject",
                    type: PropertyDataType.STRINGLIST,
                    description:
                        "Subject, keyword, classification code, or key phrase describing the resource",
                    showAlways: false,
                    required: false,
                },
                {
                    id: "7",
                    name: "Contributor",
                    type: PropertyDataType.STRINGLIST,
                    description:
                        'The institutio responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property. For software, if there is an alternate entity that "holds, archives, publishes, prints, distributes, releases, issues, or produces" the code, use the contributorType "hostingInstitution" for the code repository.',
                    showAlways: false,
                    required: false,
                },
                {
                    id: "99",
                    name: "Checkbox Test",
                    type: PropertyDataType.CHECKBOX,
                    description: "Something else",
                    showAlways: true,
                    required: false,
                    options: ["asd", "something else", "another thing"],
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
