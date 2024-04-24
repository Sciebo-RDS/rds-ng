/**
 * A single record of a project's logbook.
 *
 * @param timestamp - The timestamp of the record.
 */
export class ProjectLogbookRecord {
    public readonly timestamp: number;

    public constructor(timestamp: number) {
        this.timestamp = timestamp;
    }
}
