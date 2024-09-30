import { PropertyProfile } from "../PropertyProfile";

export const dataCite: PropertyProfile = {
    metadata: {
        id: ["DataCite", "4.5"],
        displayLabel: "DataCite",
        description: "DataCite Metadata Profile"
    },
    layout: [
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
            label: "Title",
            description: "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument.",
            input: [{ id: "title", label: "Title", type: "string" }],
            required: true,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/",
            label: "Creator",
            description:
                "The main researchers involved in producing the data, or the authors of the publication, in priority order. For instruments this is the manufacturer or developer of the instrument. To supply multiple creators, repeat this property.",
            type: ["creator"],
            required: true,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/publisher/",
            label: "Publisher",
            description:
                "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
            type: ["publisher"],
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
            example: "",
            type: ["subject"],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/",
            label: "Contributor",
            description:
                "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property.",
            example: "Charpy, Antoine; Foo Data Center",
            type: ["contributor"],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/date/",
            label: "Date",
            description: "Different dates relevant to the work.",
            type: ["date"],
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
            input: [
                { id: "resourceType", label: "Resource Type", type: "string" },
                {
                    id: "resourceTypeGeneral",
                    label: "Resource Type General",
                    type: "dropdown",
                    options: [
                        "Audiovisual",
                        "Book",
                        "BookChapter",
                        "Collection",
                        "ComputationalNotebook",
                        "ConferencePaper",
                        "ConferenceProceeding",
                        "DataPaper",
                        "Dataset",
                        "Dissertation",
                        "Event",
                        "Image",
                        "InteractiveResource",
                        "Instrument",
                        "Journal",
                        "JournalArticle",
                        "Model",
                        "OutputManagementPlan",
                        "PeerReview",
                        "PhysicalObject",
                        "Preprint",
                        "Report",
                        "Service",
                        "Software",
                        "Sound",
                        "Standard",
                        "StudyRegistration",
                        "Text",
                        "Workflow",
                        "Other"
                    ]
                }
            ],
            required: true,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/alternateidentifier/",
            label: "Alternate Identifier",
            description:
                "An identifier other than the primary Identifier applied to the resource being registered. This may be any alphanumeric string which is unique within its domain of issue. May be used for local identifiers, a serial number of an instrument or an inventory number. The AlternateIdentifier should be an additional identifier for the same instance of the resource (i.e., same location, same file).",
            example: "E-GEOD-34814",
            type: ["alternateIdentifier"],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relatedidentifier/",
            label: "Related Identifier",
            description: "Identifiers of related resources. These must be globally unique identifiers.",
            type: ["relatedIdentifier"],
            //input: [{ id: "relatedIdentifier", label: "Related Identifier", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/size/",
            label: "Size",
            description: "Size (e.g., bytes, pages, inches, etc.) or duration (extent), e.g., hours, minutes, days, etc., of a resource.",
            example: "“15 pages”, “6 MB”, “45 minutes”",
            input: [{ id: "size", label: "Size", type: "stringlist" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/format/",
            label: "Format",
            description: "Technical format of the resource. Use file extension or MIME type where possible.",
            example: "PDF, XML, MPG or application/pdf, text/xml, video/mpeg.",
            input: [{ id: "format", label: "Format", type: "stringlist" }],
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
            type: ["rights"],
            //input: [{ id: "rights", label: "Rights", type: "string" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
            label: "Description (Abstract)",
            description:
                "All additional information that does not fit in any of the other categories. May be used for technical information or detailed information associated with a scientific instrument.",
            //type: ["description"],
            input: [{ id: "abstract", label: "Description (Abstract)", type: "textarea" }],
            required: false,
            multiple: false
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation/",
            label: "Geolocation",
            description: "Spatial region or named place where the data was gathered or about which the data is focused.",
            type: ["geoLocation"],
            //input: [{ id: "geoLocation", label: "Geolocation", type: "string" }],
            required: false,
            multiple: true
        },
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/fundingreference/",
            label: "Funding Reference",
            description: "Information about financial support (funding) for the resource being registered.",
            type: ["fundingReference"],
            //input: [{ id: "fundingReference", label: "Funding Reference", type: "string" }],
            required: false,
            multiple: true
        } /* ,
        {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relateditem/",
            label: "Related Item",
            description: "Information about a resource related to the one being registered.",
            // TODO cardinality
            //linkable: [{ type: "relateditem", mulitple: true, required: false}],
            input: [{ id: "relatedItem", label: "Related Item", type: "string" }],
            required: false,
            multiple: true
        } */
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
                    description: "The full name of the creator. Format: Family name, Given names..",
                    required: true
                }
            ]
        },
        nameIdentifier: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/#nameidentifier",
            label: "Name Identifier",
            description: "Uniquely identifies an individual or legal entity, according to various schemes.",
            example: "Jane Doe",
            labelTemplate: "${nameIdentifier} (${nameIdentifierScheme})",
            input: [
                {
                    id: "nameIdentifier",
                    label: "Name Identifier",
                    type: "string"
                },
                {
                    id: "nameIdentifierScheme",
                    label: "Name Identifier Scheme",
                    type: "string",
                    description: "The name of the name identifier scheme.",
                    example: "ORCID"
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
        },
        title: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title",
            label: "Title",
            description: "A name or title by which a resource is known. May be the title of a dataset or the name of a piece of software or an instrument.",
            labelTemplate: "${title}",
            input: [
                {
                    id: "title",
                    label: "Title",
                    type: "string"
                },
                {
                    id: "titleType",
                    label: "Title Type",
                    type: "radiobuttons",
                    options: ["AlternativeTitle", "Subtitle", "TranslatedTitle", "other"],
                    description: "The type of Title (other than the Main Title)."
                }
            ]
        },
        publisher: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/publisher",
            label: "Publisher",
            description:
                "The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
            labelTemplate: "${publisher}",
            example:
                "World Data Center for Climate (WDCC), GeoForschungsZentrum Potsdam (GFZ), Consejo Superior de Investigaciones Científicas, University of Tokyo, GitHub",
            input: [
                {
                    id: "publisher",
                    label: "Publisher",
                    type: "string"
                },
                {
                    id: "publisherIdentifier",
                    label: "Publisher Identifier",
                    type: "string",
                    description: "Uniquely identifies the publisher, according to various schemes.",
                    example: "https://ror.org/04z8jg394, https://doi.org/10.17616/R3989R, https://viaf.org/viaf/151411898/, https://wikidata.org/wiki/Q7842"
                },
                {
                    id: "publisherIdentifierScheme",
                    label: "Publisher Identifier Scheme",
                    type: "string",
                    description: "The name of the publisher identifier scheme.",
                    example: "ROR, DOI, VIAF, Wikidata"
                },
                {
                    id: "schemeURI",
                    label: "Publisher Scheme URI",
                    type: "string",
                    description: "The URI of the publisher identifier scheme.",
                    example: "https://ror.org, https://doi.org, https://viaf.org, https://wikidata.org"
                }
            ]
        },
        subject: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/subject",
            label: "Subject",
            description: "Subject, keyword, classification code, or key phrase describing the resource.",
            labelTemplate: "${subject}",
            input: [
                {
                    id: "subject",
                    label: "Subject",
                    type: "string",
                    required: true
                },
                {
                    id: "subjectScheme",
                    label: "Subject Scheme",
                    type: "string",
                    description: "The name of the subject identifier scheme.",
                    example: "Library of Congress Subject Headings (LCSH), ANZSRC Fields of Research",
                    required: true
                },
                {
                    id: "schemeURI",
                    label: "Subject Scheme URI",
                    type: "string",
                    description: "The URI of the subject identifier scheme.",
                    example: "https://id.loc.gov/authorities/subjects.html"
                },
                {
                    id: "valueURI",
                    label: "Value URI",
                    type: "string",
                    description: "The URI of the subject term.",
                    example: "https://id.loc.gov/authorities/subjects/sh85035852.html",
                    required: true
                },
                {
                    id: "classificationCode",
                    label: "Classification Code",
                    type: "string",
                    description: "The classification code used for the subject term in the subject scheme.",
                    example:
                        "310607 (where 310607 is the classification code associated with the subject term “Nanobiotechnology” in the ANZSRC Fields of Research subject scheme)"
                }
            ]
        },
        contributor: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor",
            label: "Contributor",
            description:
                "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource.",
            labelTemplate: "${contributorName}",
            example: "Charpy, Antoine; Foo Data Center",
            type: ["nameIdentifier", "affiliation"],
            input: [
                {
                    id: "contributorName",
                    label: "Contributor Name",
                    type: "string",
                    description: "The full name of the contributor. Format: Family name, Given names.",
                    example: "Patel, Emily; ABC Foundation",
                    required: true
                },
                {
                    id: "nameType",
                    label: "Name Type",
                    type: "dropdown",
                    options: ["Organizational", "Personal"],
                    description: "The type of name."
                },
                {
                    id: "contributorType",
                    label: "Contributor Type",
                    type: "dropdown",
                    options: [
                        "ContactPerson",
                        "DataCollector",
                        "DataCurator",
                        "DataManager",
                        "Distributor",
                        "Editor",
                        "HostingInstitution",
                        "Producer",
                        "ProjectLeader",
                        "ProjectManager",
                        "ProjectMember",
                        "RegistrationAgency",
                        "RegistrationAuthority",
                        "RelatedPerson",
                        "Researcher",
                        "ResearchGroup",
                        "RightsHolder",
                        "Sponsor",
                        "Supervisor",
                        "WorkPackageLeader",
                        "Other"
                    ],
                    description: "The type of contributor of the resource."
                }
            ]
        },
        date: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/date",
            label: "Date",
            description: "Different dates relevant to the work. Formats: YYYY, YYYY-MM-DD, YYYY- MM-DDThh:mm:ssTZD.",
            labelTemplate: "${dateType}: ${date}",
            input: [
                {
                    id: "date",
                    label: "Date",
                    type: "date"
                },
                {
                    id: "dateType",
                    label: "Date Type",
                    type: "dropdown",
                    options: ["Accepted", "Available", "Copyrighted", "Collected", "Created", "Issued", "Submitted", "Updated", "Valid", "Withdrawn", "Other"],
                    description: "The type of date."
                },
                {
                    id: "dateInformation",
                    label: "Date Information",
                    type: "string",
                    description:
                        "Additional information about the date, if appropriate. May be used to provide more information about the publication, release, or collection date details, for example. May also be used to clarify dates in ancient history. Examples: 55 BC, 55 BCE."
                }
            ]
        },
        alternateIdentifier: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/alternateidentifier",
            label: "Alternate Identifier",
            description:
                "An identifier other than the primary Identifier applied to the resource being registered. This may be any alphanumeric string which is unique within its domain of issue. May be used for local identifiers, a serial number of an instrument or an inventory number. The AlternateIdentifier should be an additional identifier for the same instance of the resource (i.e., same location, same file).",
            labelTemplate: "${alternateIdentifier}",
            example: "E-GEOD-34814",
            input: [
                {
                    id: "alternateIdentifier",
                    label: "Alternate Identifier",
                    type: "string"
                },
                {
                    id: "alternateIdentifierType",
                    label: "Alternate Identifier Type",
                    type: "string",
                    description: "The type of the alternate identifier."
                }
            ]
        },
        relatedIdentifier: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relatedidentifier",
            label: "Related Identifier",
            description: "Identifiers of related resources. These must be globally unique identifiers.",
            example: "10.21384/bar",
            labelTemplate: "${relatedIdentifier}",
            input: [
                {
                    id: "relatedIdentifier",
                    label: "Related Identifier",
                    type: "string"
                },
                {
                    id: "relatedIdentifierType",
                    label: "Related Identifier Type",
                    type: "dropdown",
                    options: [
                        "ARK",
                        "arXiv",
                        "bibcode",
                        "DOI",
                        "EAN13",
                        "EISSN",
                        "Handle",
                        "IGSN",
                        "ISBN",
                        "ISSN",
                        "ISTC",
                        "LISSN",
                        "LSID",
                        "PMID",
                        "PURL",
                        "UPC",
                        "URL",
                        "URN",
                        "w3id"
                    ],
                    description: "The type of the related identifier."
                },
                {
                    id: "relationType",
                    label: "Relation Type",
                    type: "dropdown",
                    options: [
                        "IsCitedBy",
                        "Cites",
                        "IsSupplementTo",
                        "IsSupplementedBy",
                        "IsContinuedBy",
                        "Continues",
                        "IsDescribedBy",
                        "Describes",
                        "HasMetadata",
                        "IsMetadataFor",
                        "HasVersion",
                        "IsVersionOf",
                        "IsNewVersionOf",
                        "IsPreviousVersionOf",
                        "IsPartOf",
                        "HasPart",
                        "IsPublishedIn",
                        "IsReferencedBy",
                        "References",
                        "IsDocumentedBy",
                        "Documents",
                        "IsCompiledBy",
                        "Compiles",
                        "IsVariantFormOf",
                        "IsOriginalFormOf",
                        "IsIdenticalTo",
                        "IsReviewedBy",
                        "Reviews",
                        "IsDerivedFrom",
                        "IsSourceOf",
                        "IsRequiredBy",
                        "Requires",
                        "IsObsoletedBy",
                        "Obsoletes",
                        "IsCollectedBy",
                        "Collects"
                    ],
                    description: "The type of relationship between the resource and its related resource."
                },
                {
                    id: "relatedMetadataScheme",
                    label: "Related Metadata Scheme",
                    type: "string",
                    description: "The name of the related metadata scheme. Use only with this relation pair: (HasMetadata/ IsMetadataFor)."
                },
                {
                    id: "schemeURI",
                    label: "Scheme URI",
                    type: "string",
                    description: "The URI of the related metadata scheme. Use only with this relation pair: (HasMetadata/ IsMetadataFor)."
                },
                {
                    id: "schemeType",
                    label: "Scheme Type",
                    type: "string",
                    description: "The type of the related metadata scheme. Use only with this relation pair: (HasMetadata/ IsMetadataFor).",
                    example: "XSD, DDT, Turtle"
                },
                {
                    id: "resourceTypeGeneral",
                    label: "Resource Type General",
                    description: "The general type of the related resource.",
                    type: "dropdown",
                    options: [
                        "Audiovisual",
                        "Book",
                        "BookChapter",
                        "Collection",
                        "ComputationalNotebook",
                        "ConferencePaper",
                        "ConferenceProceeding",
                        "DataPaper",
                        "Dataset",
                        "Dissertation",
                        "Event",
                        "Image",
                        "InteractiveResource",
                        "Instrument",
                        "Journal",
                        "JournalArticle",
                        "Model",
                        "OutputManagementPlan",
                        "PeerReview",
                        "PhysicalObject",
                        "Preprint",
                        "Report",
                        "Service",
                        "Software",
                        "Sound",
                        "Standard",
                        "StudyRegistration",
                        "Text",
                        "Workflow",
                        "Other"
                    ]
                }
            ]
        },
        rights: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/rights",
            label: "Rights",
            description: "Rights information for the resource.",
            example: "Creative Commons Attribution 4.0 International; Apache License, Version 2.0",
            labelTemplate: "${rights}",
            input: [
                {
                    id: "rights",
                    label: "Rights",
                    type: "string"
                },
                {
                    id: "rightsURI",
                    label: "Rights URI",
                    type: "string",
                    description: "The URI of the license.",
                    example: "https://creativecommons.org/licenses/by/4.0/"
                },
                {
                    id: "rightsIdentifier",
                    label: "Rights Identifier",
                    type: "string",
                    description: "A short, standardized version of the license name.",
                    example: "CC-BY-3.0"
                },
                {
                    id: "rightsIdentifierScheme",
                    label: "Rights Identifier Scheme",
                    type: "string",
                    description: "The name of the scheme.",
                    example: "SPDX"
                },
                {
                    id: "schemeURI",
                    label: "Rights Scheme URI",
                    type: "string",
                    description: "The URI of the rights identifier scheme.",
                    example: "https://spdx.org/licenses/"
                }
            ]
        },
        description: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description",
            label: "Description",
            description:
                "All additional information that does not fit in any of the other categories. May be used for technical information or detailed information associated with a scientific instrument.",
            labelTemplate: "${descriptionType}",
            input: [
                {
                    id: "description",
                    label: "Description",
                    type: "textarea"
                },
                {
                    id: "descriptionType",
                    label: "Description Type",
                    type: "dropdown",
                    options: ["Abstract", "Methods", "SeriesInformation", "TableOfContents", "TechnicalInfo", "Other"],
                    description: "The type of description."
                }
            ]
        },
        geoLocation: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation",
            label: "Geolocation",
            description: "Spatial region or named place where the data was gathered or about which the data is focused.",
            labelTemplate: "${geoLocationPlace}",
            type: ["geoLocationPoint", "geoLocationBox", "geoLocationPolygon"],
            input: [
                {
                    id: "geoLocationPlace",
                    label: "Geolocation Place",
                    type: "string",
                    description: "Description of a geographic location, the named place of the resource.",
                    example: "Disko Bay"
                }
            ]
        },
        geoLocationPoint: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation/#geolocationpoint",
            label: "Geolocation Point",
            description: "A point location in space.",
            labelTemplate: "${pointLongitude}, ${pointLatitude}",
            input: [
                {
                    id: "pointLongitude",
                    label: "Longitude",
                    type: "string",
                    description: "Longitudinal dimension of point. [-180, 180]"
                },
                {
                    id: "pointLatitude",
                    label: "Latitude",
                    type: "string",
                    description: "Latitudinal dimension of point. [-90, 90]"
                }
            ]
        },
        geoLocationBox: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation/#geolocationbox",
            label: "Geolocation Box",
            description:
                "The spatial limits of a box. A box is defined by two geographic points. Left low corner and right upper corner. Each point is defined by its longitude and latitude.",
            labelTemplate: "From ${westLongitude}, ${southLatitude} to ${eastLongitude}, ${northLatitude}",
            input: [
                {
                    id: "westLongitude",
                    label: "West Longitude",
                    type: "string",
                    description: "Westernmost longitudinal dimension of the box. [-180, 180]"
                },
                {
                    id: "eastLongitude",
                    label: "East Longitude",
                    type: "string",
                    description: "Easternmost longitudinal dimension of the box. [-180, 180]"
                },
                {
                    id: "southLatitude",
                    label: "South Latitude",
                    type: "string",
                    description: "Southernmost latitudinal dimension of the box. [-90, 90]"
                },
                {
                    id: "northLatitude",
                    label: "North Latitude",
                    type: "string",
                    description: "Northernmost latitudinal dimension of the box. [-90, 90]"
                }
            ]
        },
        geoLocationPolygon: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation/#geolocationpolygon",
            label: "Geolocation Polygon",
            description: "A drawn polygon area, defined by a set of points and lines connecting the points in a closed chain.",
            labelTemplate: "Polygon with ${polygonPoints} points",
            type: ["geoLocationPoint"]
        },
        fundingReference: {
            id: "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/fundingreference",
            label: "Funding Reference",
            description: "Information about financial support (funding) for the resource being registered.",
            labelTemplate: "${funderName}, ${awardNumber}",
            input: [
                {
                    id: "funderName",
                    label: "Funder Name",
                    type: "string",
                    description: "Name of the funding provider.",
                    example: "Gordon and Betty Moore Foundation"
                },
                {
                    id: "funderIdentifier",
                    label: "Funder Identifier",
                    type: "string",
                    description: "Uniquely identifies the funder, according to various schemes.",
                    example: "https://doi.org/10.13039/100000936",
                    required: true
                },
                {
                    id: "funderIdentifierType",
                    label: "Funder Identifier Type",
                    type: "dropdown",
                    description: "The type of the funderIdentifier.",
                    options: ["Crossref Funder ID", "GRID", "ISNI", "ROR", "Other"]
                },
                {
                    id: "schemeURI",
                    label: "Funder Scheme URI",
                    type: "string",
                    description: "The URI of the funder identifier scheme.",
                    example: "https://www.crossref.org/services/funder-registry/, https://ror.org/"
                },
                {
                    id: "awardNumber",
                    label: "Award Number",
                    type: "string",
                    description: "The code assigned by the funder to a sponsored award (grant).",
                    example: "GBMF3852.01",
                    required: true
                },
                {
                    id: "awardURI",
                    label: "Award URI",
                    type: "string",
                    description: "The URI leading to a page provided by the funder for more information about the award (grant).",
                    example: "https://www.moore.org/grants/list/GBMF3859.01"
                },
                {
                    id: "awardTitle",
                    label: "Award Title",
                    type: "string",
                    description: "The human readable title or name of the award (grant).",
                    example: "Socioenvironmental Monitoring of the Amazon Basin and Xingu"
                }
            ]
        }
    }
};
