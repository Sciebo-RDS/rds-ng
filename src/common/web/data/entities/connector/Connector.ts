import { UnitID } from "../../../utils/UnitID";

/**
 * The connector ID type.
 */
export type ConnectorID = UnitID;

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

    public constructor(connectorID: ConnectorID, name: string, description: string = "") {
        this.connector_id = connectorID;

        this.name = name;
        this.description = description;
    }
}
