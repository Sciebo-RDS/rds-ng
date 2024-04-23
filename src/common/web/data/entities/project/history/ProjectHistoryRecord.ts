/**
 * A single record of a project's publishing history.
 *
 * @param timestamp - The timestamp of the record.
 */
export class ProjectHistoryRecord {
    public readonly timestamp: number;

    public constructor(timestamp: number) {
        this.timestamp = timestamp;
    }
}
