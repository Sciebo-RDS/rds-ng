import { MessageMetaInformation } from "./MessageMetaInformation";
import { type Trace } from "../Message";

class MessageMetaInformationListEntry {
    public constructor(readonly metaInformation: MessageMetaInformation,
                       readonly timeout: number = 0.0,
                       readonly timestamp: number = Date.now() / 1000.0) {
    }

    /**
     * Whether the message has timed out.
     */
    public hasTimedOut(): boolean {
        return this.timeout > 0.0 ? (Date.now() / 1000.0) - this.timestamp > this.timeout : false;
    }
}

interface MessageMetaInformationListType {
    [key: Trace]: MessageMetaInformationListEntry;
}

/**
 * List to store message meta information objects.
 */
export class MessageMetaInformationList {
    private readonly _list: MessageMetaInformationListType = {};

    /**
     * Adds a new entry to the list.
     *
     * @param unique - The unique trace identifying the message.
     * @param meta - The message meta information.
     * @param timeout - A timeout (in seconds) after which a message is deemed timed out.
     */
    public add(unique: Trace, meta: MessageMetaInformation, timeout: number): void {
        if (!(unique in this._list)) {
            this._list[unique] = new MessageMetaInformationListEntry(meta, timeout);
        }
    }

    /**
     * Removes an entry from the list.
     *
     * @param unique - The unique trace identifying the message.
     */
    public remove(unique: Trace): void {
        if (unique in this._list) {
            delete this._list[unique];
        }
    }

    /**
     * Finds an entry associated with the given ``unique``.
     *
     * @param unique - The unique trace identifying the message.
     *
     * @returns - The found meta information, if any.
     */
    public find(unique: Trace): MessageMetaInformation | null {
        if (unique in this._list) {
            return this._list[unique].metaInformation;
        }

        return null;
    }

    /**
     * Finds all entries that have timed out already.
     *
     * @returns - A list of all timed out entries.
     */
    public findTimedOutEntries(): Trace[] {
        let entries: Trace[] = [];
        for (const [unique, entry] of Object.entries(this._list)) {
            if (entry.hasTimedOut()) {
                entries.push(unique);
            }
        }
        return entries;
    }
}
