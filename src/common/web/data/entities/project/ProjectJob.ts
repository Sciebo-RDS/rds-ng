import { ConnectorInstanceID } from "../connector/ConnectorInstance";
import { ProjectID } from "./Project";

/**
 * A project (publishing) job that is currently active.
 *
 * @param project_id - The project ID.
 * @param connector_instance - The connector instance ID.
 * @param timestamp - The starting time.
 * @param progress - The total progress (0.0 - 1.0).
 * @param message - The current activity message.
 */
export class ProjectJob {
    public readonly project_id: ProjectID;
    public readonly connector_instance: ConnectorInstanceID;

    public readonly timestamp: number;

    public readonly progress: number;
    public readonly message: string;

    constructor(projectID: ProjectID, connectorInstance: ConnectorInstanceID, timestamp: number, progress: number = 0.0, message: string = "") {
        this.project_id = projectID;
        this.connector_instance = connectorInstance;

        this.timestamp = timestamp;

        this.progress = progress;
        this.message = message;
    }
}
