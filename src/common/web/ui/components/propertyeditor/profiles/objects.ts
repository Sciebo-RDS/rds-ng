import { type PropertyProfile } from "../PropertyProfile";

export const objects: PropertyProfile = {
    metadata: {
        id: ["objects", "2024.09.17"],
        displayLabel: "File description",
        description: "A Profile for individual resources."
    },
    layout: [
        {
            id: "comment",
            label: "Comment",
            description: "Descriptive comment about the file object.",
            input: [
                {
                    id: "comment",
                    label: "Comment",
                    type: "textarea",
                }
            ],
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
                    description: "The full name of the creator."
                }
            ]
        },
        nameIdentifier: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/#nameidentifier",
            label: "Name Identifier",
            description: "Uniquely identifies an individual or legal entity, according to various schemes.",
            example: "Jane Doe",
            labelTemplate: "${nameIdentifier}",
            input: [
                {
                    id: "nameIdentifier",
                    label: "Name Identifier",
                    type: "string",
                    description: "Uniquely identifies an individual or legal entity, according to various schemes."
                },
                {
                    id: "nameIdentifierScheme",
                    label: "Name Identifier Scheme",
                    type: "string",
                    description: "The name of the name identifier scheme."
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