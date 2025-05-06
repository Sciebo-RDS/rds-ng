import { type ConnectorInstanceID } from "../connector/ConnectorInstance";
import { type UserID } from "../user/User";
import { type ProjectID } from "./Project";

/**
 * A project job that is currently active.
 *
 * @param user_id - The ID of the user the job belongs to.
 * @param project_id - The project ID.
 * @param connector_instance - The connector instance ID.
 * @param timestamp - The starting time.
 * @param progress - The total progress (0.0 - 1.0).
 * @param message - The current activity message.
 */
export class ProjectJob {
    public readonly user_id: UserID;
    public readonly project_id: ProjectID;
    public readonly connector_instance: ConnectorInstanceID;

    public readonly timestamp: number;

    public readonly progress: number;
    public readonly message: string;

    constructor(userID: UserID, projectID: ProjectID, connectorInstance: ConnectorInstanceID, timestamp: number, progress: number = 0.0, message: string = "") {
        this.user_id = userID;
        this.project_id = projectID;
        this.connector_instance = connectorInstance;

        this.timestamp = timestamp;

        this.progress = progress;
        this.message = message;
    }
}
