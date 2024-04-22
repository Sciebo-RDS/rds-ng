/*
 * The status of the publishing operation.
 */
export const enum ProjectHistoryRecordStatus {
    Done = 0,
    Failed = -1,
}

/**
 * A single record of a project's publishing history.
 */
export class ProjectHistoryRecord {
    public readonly timestamp: number;

    public readonly status: ProjectHistoryRecordStatus;
    public readonly message: string;

    public constructor(timestamp: number, status: ProjectHistoryRecordStatus, message: string) {
        this.timestamp = timestamp;

        this.status = status;
        this.message = message;
    }
}
