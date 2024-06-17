import { AuthorizationState } from "../authorization/AuthorizationState";
import { type ConnectorID } from "./Connector";

/**
 * The connector instance ID type.
 */
export type ConnectorInstanceID = string;

/**
 * A configured connector instance (i.e., a connector the user has added to his configuration).
 *
 * @param instance_id - The ID of the connector instance.
 * @param connector_id - The assigned connector.
 * @param name - The name of this connector instance.
 * @param description - The instance description.
 * @param authorization_state: The authorization state.
 */
export class ConnectorInstance {
    public readonly instance_id: ConnectorInstanceID;

    public readonly connector_id: ConnectorID;

    public readonly name: string;
    public readonly description: string;

    public readonly authorization_state: AuthorizationState;

    public constructor(
        instanceID: ConnectorInstanceID,
        connectorID: ConnectorID,
        name: string,
        description: string = "",
        authState: AuthorizationState = AuthorizationState.NotAuthorized,
    ) {
        this.instance_id = instanceID;

        this.connector_id = connectorID;

        this.name = name;
        this.description = description;

        this.authorization_state = authState;
    }
}
