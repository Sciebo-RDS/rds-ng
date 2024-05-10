/**
 * A single record of a project's logbook.
 *
 * @param record - The record entry ID.
 * @param timestamp - The timestamp of the record.
 * @param seen - Whether the record has been seen by the user.
 */
export class ProjectLogbookRecord {
    public readonly record: number;
    public readonly timestamp: number;

    public readonly seen: boolean;

    public constructor(record: number, timestamp: number, seen: boolean = false) {
        this.record = record;
        this.timestamp = timestamp;

        this.seen = seen;
    }
}
