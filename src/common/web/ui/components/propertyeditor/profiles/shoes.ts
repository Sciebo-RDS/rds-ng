import { type Profile } from "../PropertyProfile";

export const shoes: Profile = {
    metadata: {
        id: ["Shoes", "2024.2.21"],
        name: "Shoes",
        version: "2024.2.21",
        description: "A Profile for individual resources."
    },
    layout: [
        {
            id: "Shoe",
            label: "Shoe",
            description: "Shoe descriptions",
            input: [
                {
                    id: "Name",
                    label: "Name",
                    type: "string",
                    description: "The name of the shoes."
                },
                {
                    id: "ShoeType",
                    label: "Type",
                    type: "dropdown",
                    description: "The type of the shoes.",
                    options: ["nice shoes", "fancy shoes", "shoey shoes"]
                },
                {
                    id: "Description",
                    label: "Description",
                    type: "textarea",
                    description: "The shoes' description."
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
