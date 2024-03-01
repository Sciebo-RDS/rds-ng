import { type PropertyProfile, PropertyDataType } from "../PropertyProfile";

export const osf: PropertyProfile = {
    profile_id: { name: "OSF", version: "2024.2.1" },
    categories: [
        {
            id: "Mandatory",
            name: "Mandatory",
            description: "Mandatory OSF properties",
            properties: [
                {
                    id: "Title",
                    name: "Title",
                    type: PropertyDataType.STRING,
                    description:
                        "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument.",
                    showAlways: true,
                    required: true,
                },
                {
                    id: "OsfCategory",
                    name: "Category",
                    type: PropertyDataType.DROPDOWN,
                    description:
                        "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
                    showAlways: true,
                    required: true,
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
                        "other",
                    ],
                },
                {
                    id: "Description",
                    name: "Description",
                    type: PropertyDataType.TEXTAREA,
                    description: "The Description of you resource.",
                    showAlways: true,
                    required: true,
                },
            ],
        },
    ],
};
