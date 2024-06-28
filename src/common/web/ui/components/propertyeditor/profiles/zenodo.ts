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
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
            label: "Title",
            description: "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument.",
            //type: ["title"],
            input: [{ id: "title", label: "Title", type: "string" }],
            required: true,
            multiple: true
        },
        {
            id: "ZenodoCategory",
            label: "Zenodo Category",
            input: [{ id: "category", label: "Zenodo Category", type: "dropdown", options: ["shoes", "nice shoes", "fancy shoes"] }],
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
