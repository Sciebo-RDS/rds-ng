/*
 * The status of the publishing operation.
 */
import { type ConnectorInstanceID } from "../../connector/ConnectorInstance";
import { ProjectHistoryRecord } from "./ProjectHistoryRecord";

export const enum PublishingHistoryRecordStatus {
    Done = 0,
    Failed = -1,
}

/**
 * A single record of a project's publishing history.
 *
 * @param status - The status (done or failed).
 * @param message - An optional message (usually in case of an error).
 */
export class PublishingHistoryRecord extends ProjectHistoryRecord {
    public readonly connector_instance: ConnectorInstanceID;

    public readonly status: PublishingHistoryRecordStatus;
    public readonly message: string;

    public constructor(timestamp: number, connectorInstance: ConnectorInstanceID, status: PublishingHistoryRecordStatus, message: string) {
        super(timestamp);

        this.connector_instance = connectorInstance;

        this.status = status;
        this.message = message;
    }
}
