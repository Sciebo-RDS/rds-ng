import { Type } from "class-transformer";

import { ConnectorInstance } from "../connector/ConnectorInstance";

/**
 * User settings (i.e., the settings a user configures in the UI) data.
 *
 * @param connector_instances - A list of all configured connector instances.
 */
export class UserSettings {
    // @ts-ignore
    @Type(() => ConnectorInstance)
    public readonly connector_instances: ConnectorInstance[] = [];

    public constructor(connectorInstances: ConnectorInstance[] = []) {
        this.connector_instances = connectorInstances;
    }
}
