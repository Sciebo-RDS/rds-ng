/**
 * All known component types.
 */
export const enum ComponentType {
    Infrastructure = "infra",
    Web = "web"
}

/**
 * All known component units.
 */
export const enum ComponentUnit {
    // Infrastructure
    Server = "server",
    Connector = "connector",
    Domo = "domo",

    // Web
    Frontend = "frontend"
}
