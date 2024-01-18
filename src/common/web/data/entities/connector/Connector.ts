import { Type } from "class-transformer";

/**
 * The connector ID type.
 */
export type ConnectorID = string;

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
 * @param name - The name of the connector.
 * @param description - An optional connector description.
 */
export class Connector {
    public readonly connector_id: ConnectorID;

    public readonly name: string;
    public readonly description: string;

    // @ts-ignore
    @Type(() => ConnectorLogos)
    public readonly logos: ConnectorLogos;

    public constructor(connectorID: ConnectorID, name: string, description: string = "", logos: ConnectorLogos = new ConnectorLogos()) {
        this.connector_id = connectorID;

        this.name = name;
        this.description = description;

        this.logos = logos;
    }
}
