import { SemVer } from "semver";

export type ProfileName = string;

export type PropertyProfile = {
  version: SemVer;
  name: ProfileName;
  categories: PropertyCategory[];
};

//categories should rather be subprofiles?
export type PropertyCategory = {
  name: string | null;
  properties: (Property | SelectionProperty)[];
};

export type Property = {
  name: string;
  type: PropertyDataType;
  description: string;
  required: boolean;
  component: string;
  default?: boolean;
  filter?: string[];
};

export type SelectionProperty = Property & {
  options: string[];
};

export type PropertyDataType = "string" | "number" | "boolean" | "selection";

export class PropertySet {
  private _profile: PropertyProfile;
  private _categories: PropertyCategory[];
}

export const testProfile: PropertyProfile = {
  version: "1.1.1",
  name: "Test Profile",
  categories: [
    {
      name: "General",
      properties: [
        {
          name: "Author",
          type: "string",
          description: "The Authors name",
          required: true,
          component: "something",
          default: true,
        },
      ],
    },
    {
      name: "OSF",
      properties: [
        {
          name: "Number of Authors",
          type: "selection",
          description:
            "How many authors were there?How many authors were there?How many authors were there?How many authors were there?",
          required: true,
          component: "something",
          default: true,
          options: ["asd", "asd"],
        },
        {
          name: "Number of Authors",
          type: "number",
          description: "The number of authors",
          required: true,
          component: "something",
          default: false,
        },
        {
          name: "Names of Authors",
          type: "string",
          description: "The Authors name",
          required: true,
          component: "something",
        },
      ],
    },
  ],
};
