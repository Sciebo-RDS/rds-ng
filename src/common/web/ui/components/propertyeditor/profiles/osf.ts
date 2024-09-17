import { type PropertyProfile } from "../PropertyProfile";

export const osf: PropertyProfile = {
    metadata: {
        id: ["OSF", "2024.2.21"],
        displayLabel: "OSF",
        description: "A Profile for OSF DMP."
    },
    layout: [
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
            label: "Title",
            description: "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument.",
            //type: ["title"],
            input: [{ id: "title", label: "Title", type: "string" }],
            required: true,
            multiple: true
        },
        {
            id: "OsfCategory",
            label: "OSF Category",
            input: [
                {
                    id: "category",
                    label: "OSF Category",
                    type: "dropdown",
                    options: [
                        "analysis",
                        "communication",
                        "data",
                        "hypothesis",
                        "instrumentation",
                        "methods and measures",
                        "procedure",
                        "project",
                        "software",
                        "other"
                    ]
                }
            ],
            description:
                "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
            required: true,
            multiple: true
        },
        {
            id: "Description",
            label: "Description",
            input: [{ id: "description", label: "Description", type: "textarea" }],
            description: "The Description of your resource.",
            required: true,
            multiple: true
        }
    ]
};
