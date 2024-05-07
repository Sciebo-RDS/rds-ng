/**
 * A single record of a project's logbook.
 *
 * @param timestamp - The timestamp of the record.
 * @param seen - Whether the record has been seen by the user.
 */
export class ProjectLogbookRecord {
    public readonly timestamp: number;

    public readonly seen: boolean;

    public constructor(timestamp: number, seen: boolean = false) {
        this.timestamp = timestamp;

        this.seen = seen;
    }
}
