import { Profile } from "../PropertyProfile";

export const zenodo: Profile = {
    metadata: {
        id: ["Zenodo", "0.0.1"],
        name: "Zenodo",
        version: "0.0.1",
        description: "A Profile for Zenodo."
    },
    layout: [
        {
            id: "Mandatory",
            label: "Mandatory",
            description: "Mandatory Zenodo properties",
            input: [
                {
                    id: "Title",
                    label: "Title",
                    type: "string",
                    description:
                        "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument."
                },
                {
                    id: "ZenodoCategory",
                    label: "Category",
                    type: "dropdown",
                    description:
                        "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",

                    options: ["shoes", "nice shoes", "fancy shoes"]
                },
                {
                    id: "Description",
                    label: "Description",
                    type: "textarea",
                    description: "The Description of your resource."
                }
            ]
        }
    ]
};
