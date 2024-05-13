import { type ConnectorInstanceID } from "../../connector/ConnectorInstance";
import { ProjectLogbookRecord, type RecordID } from "./ProjectLogbookRecord";

/**
 * A single record of a project's job history.
 *
 * @param connector_instance - The connector instance ID.
 * @param status - The success status (done or failed).
 * @param message - An optional message (usually in case of an error).
 */
export class ProjectJobHistoryRecord extends ProjectLogbookRecord {
    public readonly connector_instance: ConnectorInstanceID;

    public readonly success: boolean;
    public readonly message: string;

    public constructor(record: RecordID, timestamp: number, connectorInstance: ConnectorInstanceID, success: boolean, message: string) {
        super(record, timestamp);

        this.connector_instance = connectorInstance;

        this.success = success;
        this.message = message;
    }
}
