import { type Profile } from "./PropertyProfile";

export const testProfile: Profile = {
    metadata: {
        id: ["TestProfile", "1.1"],
        name: "Test Profile",
        version: "1.1",
        description: "Test stuff"
    },
    layout: [
        {
            id: "Author",
            label: "Author",
            description: "The Authors name",
            input: [{ id: "Author", label: "Authorname", type: "string" }],
            type: ["creator"],
            required: true,
            multiple: true
        },
        {
            id: "NumberOfAuthors",
            label: "Number of Authors",
            description:
                "This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! This is a very looooooooong description that should be wrapped! ",
            required: true,
            input: [{ id: "NumberOfAuthors", label: "Number of Authors", type: "number" }]
        },
        {
            id: "SomeMultiselect",
            label: "Some Multiselect",
            description: "Here are some options",
            input: [{ id: "SomeMultiselect", label: "Some Multiselect", type: "multiselect", options: ["asd", "something else", "another thing"] }],
            required: true
        },
        {
            id: "Radio",
            label: "Some Radio Buttons",
            description: "Here are some Radio Buttons",
            input: [{ id: "Radio", label: "Some Radio Buttons", type: "radiobuttons", options: ["asd", "something else", "another thing"] }],
            required: true
        },
        {
            id: "checkbox",
            label: "A checkbox",
            description: "Here are some Radio Buttons",
            input: [{ id: "checkbox", label: "A checkbox", type: "checkbox", options: ["asd", "something else", "another thing"] }],
            required: true
        },
        {
            id: "number",
            label: "Number",
            description: "The number of authors",
            input: [{ id: "number", label: "Number", type: "number" }],
            required: true
        },
        {
            id: "authors",
            label: "Authors",
            description: "The Authors name",
            input: [{ id: "authors", label: "Authors", type: "textarea" }],
            required: true
        },
        {
            id: "authorslist",
            label: "Authors list",
            description: "Comma separated list of authors",
            input: [{ id: "authorslist", label: "Authors list", type: "stringlist" }],
            required: true
        },
        {
            id: "publishdate",
            label: "Publishing date",
            description: "When was this made publicly available?",
            input: [{ id: "publishdate", label: "Publishing date", type: "date" }],
            required: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/",
            label: "Creator",
            description:
                "The main researchers involved in producing the data, or the authors of the publication, in priority order. For instruments this is the manufacturer or developer of the instrument. To supply multiple creators, repeat this property.",
            type: ["creator"],
            required: true,
            multiple: true
        }
    ],
    classes: {
        creator: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/",
            label: "Creator",
            description:
                "The main researchers involved in producing the data, or the authors of the publication, in priority order. For instruments this is the manufacturer or developer of the instrument. To supply multiple creators, repeat this property.",
            labelTemplate: "${name}",
            type: ["nameIdentifier", "affiliation"],
            input: [
                {
                    id: "name",
                    label: "Name",
                    type: "string",
                    description: "The full name of the creator. Format: Family name, Given names.."
                }
            ]
        },
        nameIdentifier: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/#nameidentifier",
            label: "Name Identifier",
            description: "Uniquely identifies an individual or legal entity, according to various schemes.",
            example: "Jane Doe",
            labelTemplate: "${nameIdentifier} (${nameIdentifierScheme})",
            input: [
                {
                    id: "nameIdentifier",
                    label: "Name Identifier",
                    type: "string"
                },
                {
                    id: "nameIdentifierScheme",
                    label: "Name Identifier Scheme",
                    type: "string",
                    description: "The name of the name identifier scheme.",
                    example: "ORCID"
                },
                {
                    id: "schemeURI",
                    label: "Scheme URI",
                    type: "string",
                    description: "The URI of the name identifier scheme."
                }
            ]
        },
        affiliation: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/#affiliation",
            label: "Affiliation",
            labelTemplate: "${affiliation}",
            input: [
                {
                    id: "affiliation",
                    label: "Affiliation",
                    type: "string",
                    description: "The organizational or institutional affiliation of the creator."
                },
                {
                    id: "affiliationIdentifier",
                    label: "Affiliation Identifier",
                    type: "string",
                    description: "Uniquely identifies the organizational affiliation of the creator."
                },
                {
                    id: "affiliationIdentifierScheme",
                    label: "Affiliation Identifier Scheme",
                    type: "string",
                    description: "The name of the affiliation identifier scheme."
                },
                {
                    id: "schemeURI",
                    label: "Affiliation Scheme URI",
                    type: "string",
                    description: "The URI of the affiliation identifier scheme."
                }
            ]
        }
    }
};
