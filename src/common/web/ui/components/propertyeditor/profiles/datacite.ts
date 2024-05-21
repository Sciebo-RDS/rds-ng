export const dataCite: {
    metadata: {
        id: [string, number];
        name: string;
        description: string;
        version: number;
    };
    layout: {
        id: string;
        label: string;
        description: string;
        example?: string;
        type?: string[];
        input?: { id: string; label: string; type: string }[];
        required: boolean;
        multiple: boolean;
    }[];
    classes: {};
} = {
    metadata: {
        id: ["DataCite", 4.5],
        name: "DataCite Profile",
        description: "DataCite Metadata Profile",
        version: 4.5
    },
    layout: [
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/identifier/",
            label: "Identifier",
            description: "The Identifier is a unique string that identifies a resource. Should be a URL or a DOI.",
            example: "https://doi.org/10.1234/abc",
            input: [
                { id: "identifier", label: "Identifier", type: "string" },
                { id: "test", label: "test", type: "string" }
            ],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/",
            label: "Creator",
            description:
                "The main researchers involved in producing the data, or the authors of the publication, in priority order. For instruments this is the manufacturer or developer of the instrument. To supply multiple creators, repeat this property.",
            type: ["creator", "nameIdentifier", "affiliation"],
            required: true,
            multiple: true
        },
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
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/publisher/",
            label: "Publisher",
            description:
                "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
            //type: ["publisher"],
            input: [{ id: "publisher", label: "Publisher", type: "string" }],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/publicationyear/",
            label: "Publication Year",
            description: "The year when the data was or will be made publicly available. Format: YYYY.",
            example: "2018",
            input: [{ id: "publicationYear", label: "Publication Year", type: "number" }],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/subject/",
            label: "Subject",
            description: "Subject, keyword, classification code, or key phrase describing the resource.",
            example:
                "World Data Center for Climate (WDCC), GeoForschungsZentrum Potsdam (GFZ), Consejo Superior de Investigaciones Científicas, University of Tokyo, GitHub",
            //type: ["subject"],
            input: [{ id: "subject", label: "Subject", type: "string" }],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/",
            label: "Contributor",
            description:
                "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property.",
            example: "Charpy, Antoine; Foo Data Center",
            //type: ["contributor"],
            input: [{ id: "contributor", label: "Contributor", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/date/",
            label: "Date",
            description: "Different dates relevant to the work.",
            //type: ["date"],
            input: [{ id: "date", label: "Date", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/language/",
            label: "Language",
            description: "The primary language of the resource.",
            example: "en, fr",
            input: [{ id: "language", label: "Language", type: "string" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/resourcetype/",
            label: "Resource Type",
            description:
                "A description of the resource. The recommended content is a single term of some detail so that a pair can be formed with the resourceTypeGeneral sub-property. For example, a resourceType of “Census Data” paired with a resourceTypeGeneral of “Dataset” yields “Dataset/Census Data”.",
            example: "Census Data",
            //type: ["resourceType"],
            input: [{ id: "resourceType", label: "Resource Type", type: "string" }],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/alternateidentifier/",
            label: "Alternate Identifier",
            description:
                "An identifier other than the primary Identifier applied to the resource being registered. This may be any alphanumeric string which is unique within its domain of issue. May be used for local identifiers, a serial number of an instrument or an inventory number. The AlternateIdentifier should be an additional identifier for the same instance of the resource (i.e., same location, same file).",
            example: "E-GEOD-34814",
            //type: ["alternateIdentifier"],
            input: [{ id: "alternateIdentifier", label: "Alternate Identifier", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relatedidentifier/",
            label: "Related Identifier",
            description: "Identifiers of related resources. These must be globally unique identifiers.",
            //type: ["relatedIdentifier"],
            input: [{ id: "relatedIdentifier", label: "Related Identifier", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/size/",
            label: "Size",
            description: "Size (e.g., bytes, pages, inches, etc.) or duration (extent), e.g., hours, minutes, days, etc., of a resource.",
            example: "“15 pages”, “6 MB”, “45 minutes”",
            input: [{ id: "size", label: "Size", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/format/",
            label: "Format",
            description: "Technical format of the resource. Use file extension or MIME type where possible.",
            example: "PDF, XML, MPG or application/pdf, text/xml, video/mpeg.",
            input: [{ id: "format", label: "Format", type: "string" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/version/",
            label: "Version",
            description:
                "The version number of the resource. Suggested practice: track major_version.minor_version. Register a new identifier for a major version change.",
            example: "2.1",
            input: [{ id: "version", label: "Version", type: "string" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/rights/",
            label: "Rights",
            description: "Rights information for the resource.",
            //type: ["rights"],
            input: [{ id: "rights", label: "Rights", type: "string" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
            label: "Description",
            description:
                "All additional information that does not fit in any of the other categories. May be used for technical information or detailed information associated with a scientific instrument.",
            //type: ["description"],
            input: [{ id: "description", label: "Description", type: "string" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation/",
            label: "Geolocation",
            description: "Spatial region or named place where the data was gathered or about which the data is focused.",
            //type: ["geoLocation"],
            input: [{ id: "geoLocation", label: "Geolocation", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/fundingreference/",
            label: "Funding Reference",
            description: "Information about financial support (funding) for the resource being registered.",
            //type: ["fundingReference"],
            input: [{ id: "fundingReference", label: "Funding Reference", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relateditem/",
            label: "Related Item",
            description: "Information about a resource related to the one being registered.",
            //type: ["relateditem"],
            input: [{ id: "relatedItem", label: "Related Item", type: "string" }],
            required: false,
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
            type: ["creator"],
            input: [
                {
                    id: "name",
                    label: "Name",
                    type: "string"
                },
                {
                    id: "lang",
                    label: "Language",
                    type: "string"
                },
                {
                    id: "nameType",
                    label: "Name Type",
                    type: "select",
                    options: ["Personal", "Organizational"]
                },
                {
                    id: "givenName",
                    label: "Given Name",
                    type: "string"
                },
                {
                    id: "familyName",
                    label: "Family Name",
                    type: "string"
                },
                {
                    id: "nameIdentifier",
                    label: "Name Identifier",
                    type: "nameIdentifier",
                    multiple: true
                },
                {
                    id: "affiliation",
                    label: "Affiliation",
                    type: "affiliation",
                    multiple: true
                }
            ]
        },
        nameIdentifier: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/#nameidentifier",
            label: "Name Identifier",
            labelTemplate: "${nameIdentifier}",
            input: [
                {
                    id: "nameIdentifier",
                    label: "Name Identifier",
                    type: "string"
                },
                {
                    id: "nameIdentifierScheme",
                    label: "Name Identifier Scheme",
                    type: "string"
                },
                {
                    id: "schemeURI",
                    label: "Scheme URI",
                    type: "string"
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
                    type: "string"
                },
                {
                    id: "affiliationIdentifier",
                    label: "Affiliation Identifier",
                    type: "string"
                },
                {
                    id: "affiliationIdentifierScheme",
                    label: "Affiliation Identifier Scheme",
                    type: "string"
                },
                {
                    id: "schemeURI",
                    label: "Affiliation Scheme URI",
                    type: "string"
                }
            ]
        }
    }
};
