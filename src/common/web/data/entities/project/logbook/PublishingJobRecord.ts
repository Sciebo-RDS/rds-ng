import { type ConnectorInstanceID } from "../../connector/ConnectorInstance";
import { ProjectLogbookRecord } from "./ProjectLogbookRecord";

/**
 * A single record of a project's running publication job.
 *
 * @param connector_instance - The connector instance ID.
 * @param progress - The total progress (0.0 - 1.0).
 * @param message - The current activity message.
 */
export class PublishingJobRecord extends ProjectLogbookRecord {
    public readonly connector_instance: ConnectorInstanceID;

    public readonly progress: number;
    public readonly message: string;

    public constructor(timestamp: number, connectorInstance: ConnectorInstanceID, progress: number, message: string) {
        super(timestamp);

        this.connector_instance = connectorInstance;

        this.progress = progress;
        this.message = message;
    }
}
