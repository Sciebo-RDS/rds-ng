import { type PropertyProfile, PropertyDataType } from "../PropertyProfile";

export const resources: PropertyProfile = {
    profile_id: { name: "Resources", version: "2024.2.21" },
    categories: [
        {
            id: "Shoes",
            name: "Shoes",
            description: "Shoe descriptions",
            properties: [
                {
                    id: "Name",
                    name: "Name",
                    type: PropertyDataType.STRING,
                    description:
                        "The name of the shoes.",
                    showAlways: true,
                    required: true
                },
                {
                    id: "ShoeType",
                    name: "Type",
                    type: PropertyDataType.DROPDOWN,
                    description:
                        "The type of the shoes.",
                    showAlways: true,
                    required: true,
                    options: [
                        "nice shoes",
                        "fancy shoes",
                        "shoey shoes"
                    ]
                },
                {
                    id: "Description",
                    name: "Description",
                    type: PropertyDataType.TEXTAREA,
                    description: "The shoes' description.",
                    showAlways: true,
                    required: false
                }
            ]
        }
    ]
};
