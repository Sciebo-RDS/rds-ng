/*
 * The status of the publishing operation.
 */
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
    public readonly status: PublishingHistoryRecordStatus;
    public readonly message: string;

    public constructor(timestamp: number, status: PublishingHistoryRecordStatus, message: string) {
        super(timestamp);

        this.status = status;
        this.message = message;
    }
}
