import { type Profile } from "../PropertyProfile";

export const osf: Profile = {
    metadata: {
        id: ["OSF", "2024.2.21"],
        name: "OSF",
        version: "2024.2.21",
        description: "A Profile for OSF DMP."
    },
    layout: [
        {
            id: "Mandatory",
            label: "Mandatory",
            description: "Mandatory OSF properties",
            input: [
                {
                    id: "Title",
                    label: "Title",
                    type: "string",
                    description:
                        "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument."
                },
                {
                    id: "OsfCategory",
                    label: "Category",
                    type: "dropdown",
                    description:
                        "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",

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
                },
                {
                    id: "Description",
                    label: "Description",
                    type: "textarea",
                    description: "The Description of you resource."
                }
            ]
        }
    ]
};
