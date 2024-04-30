import { type ConnectorInstanceID } from "../../connector/ConnectorInstance";
import { ProjectLogbookRecord } from "./ProjectLogbookRecord";

/*
 * The status of the job operation.
 */
export const enum ProjectJobHistoryRecordStatus {
    Done = 0,
    Failed = -1,
}

/**
 * A single record of a project's job history.
 *
 * @param connector_instance - The connector instance ID.
 * @param status - The status (done or failed).
 * @param message - An optional message (usually in case of an error).
 */
export class ProjectJobHistoryRecord extends ProjectLogbookRecord {
    public readonly connector_instance: ConnectorInstanceID;

    public readonly status: ProjectJobHistoryRecordStatus;
    public readonly message: string;

    public constructor(timestamp: number, connectorInstance: ConnectorInstanceID, status: ProjectJobHistoryRecordStatus, message: string) {
        super(timestamp);

        this.connector_instance = connectorInstance;

        this.status = status;
        this.message = message;
    }
}