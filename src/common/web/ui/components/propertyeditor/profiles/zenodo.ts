import { type PropertyProfile, PropertyDataType } from "../PropertyProfile";

export const osf: PropertyProfile = {
    profile_id: { name: "Zenodo", version: "0.0.1" },
    categories: [
        {
            id: "Mandatory",
            name: "Mandatory",
            description: "Mandatory Zenodo properties",
            properties: [
                {
                    id: "Title",
                    name: "Title",
                    type: PropertyDataType.STRING,
                    description:
                        "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument.",
                    showAlways: true,
                    required: true
                },
                {
                    id: "ZenodoCategory",
                    name: "Category",
                    type: PropertyDataType.DROPDOWN,
                    description:
                        "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
                    showAlways: true,
                    required: true,
                    options: [
                        "shoes",
                        "nice shoes",
                        "fancy shoes"
                    ]
                },
                {
                    id: "Description",
                    name: "Description",
                    type: PropertyDataType.TEXTAREA,
                    description: "The Description of your resource.",
                    showAlways: true,
                    required: true
                }
            ]
        }
    ]
};
