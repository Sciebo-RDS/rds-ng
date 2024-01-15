import { type ConnectorID } from "./Connector";

/**
 * The connector instance ID type.
 */
export type ConnectorInstanceID = number;

/**
 * A configured connector instance (i.e., a connector the user has added to his configuration).
 *
 * @param instance_id - The ID of the connector instance.
 * @param connector_id - The assigned connector.
 * @param name - The name of this connector instance.
 */
export class ConnectorInstance {
    public readonly instance_id: ConnectorInstanceID;

    public readonly connector_id: ConnectorID;

    public readonly name: string;

    public constructor(instanceID: ConnectorInstanceID, connectorID: ConnectorID, name: string) {
        this.instance_id = instanceID;

        this.connector_id = connectorID;

        this.name = name;
    }
}
