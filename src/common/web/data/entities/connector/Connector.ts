import { Type } from "class-transformer";

import { PropertyProfile } from "../../../ui/components/propertyeditor/PropertyProfile";
import { UnitID } from "../../../utils/UnitID";
import { type AuthorizationSettings } from "../authorization/AuthorizationSettings";

/**
 * The connector ID type.
 */
export type ConnectorID = string;

/**
 * The connector category type.
 */
export type ConnectorCategoryID = string;

/**
 * Various options of a category.
 *
 * @param PublishOnce - If set, the project may only be published once.
 */
export const enum ConnectorOptions {
    Default = 0x0000,
    PublishOnce = 0x0001
}

/**
 * Base64-encoded image data of the connector logos.
 *
 * @param default_logo - The default logo.
 * @param horizontal_logo - A logo with small height used specifically for horizontal display.
 */
export class ConnectorLogos {
    public readonly default_logo: string | undefined = undefined;
    public readonly horizontal_logo: string | undefined = undefined;

    public constructor(defaultLogo?: string, horizontalLogo?: string) {
        this.default_logo = defaultLogo;
        this.horizontal_logo = horizontalLogo;
    }
}

/**
 * Data for a single **Connector**.
 *
 * @param connector_id - The unique connector identifier.
 * @param connector_address - The target address of the connector.
 * @param category - The connector category.
 * @param name - The name of the connector.
 * @param description - An optional connector description.
 * @param authorization - Authorization settings for the connector.
 * @param options - The connector options.
 * @param logos - Image data of the connector logos.
 * @param metadata_profile - The profile for connector-specific data.
 * @param announce_timestamp - The timestamp when the connector was last announced.
 */
export class Connector {
    public readonly connector_id: ConnectorID;
    // @ts-ignore
    @Type(() => UnitID)
    public readonly connector_address: UnitID;

    public readonly name: string;
    public readonly description: string;
    public readonly category: ConnectorCategoryID;

    public readonly authorization: AuthorizationSettings;
    public readonly options: ConnectorOptions;

    // @ts-ignore
    @Type(() => ConnectorLogos)
    public readonly logos: ConnectorLogos;

    // @ts-ignore
    @Type(() => PropertyProfile)
    public readonly metadata_profile: PropertyProfile;

    public readonly announce_timestamp: Number = 0.0;

    public constructor(
        connectorID: ConnectorID,
        connectorAddress: UnitID,
        name: string,
        description: string,
        category: ConnectorCategoryID,
        authorization: AuthorizationSettings = { strategy: "", config: {} },
        options: ConnectorOptions = ConnectorOptions.Default,
        logos: ConnectorLogos = new ConnectorLogos(),
        metadataProfile: PropertyProfile = new PropertyProfile({ id: ["", ""], displayLabel: "", description: "" }, [])
    ) {
        this.connector_id = connectorID;
        this.connector_address = connectorAddress;

        this.name = name;
        this.description = description;
        this.category = category;

        this.authorization = authorization;
        this.options = options;

        this.logos = logos;

        this.metadata_profile = metadataProfile;
    }
}
