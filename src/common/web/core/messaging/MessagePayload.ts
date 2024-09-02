export type PayloadData = any;
export type Payload = Record<string, PayloadData>;

/**
 * Class holding arbitrary payload data (as key-value pairs) of a message.
 */
export class MessagePayload {
    private _payload: Payload = {};

    /**
     * Sets a payload item.
     * @param key - The key of the item.
     * @param data - The item data.
     */
    public set(key: string, data: PayloadData) {
        this._payload[key] = data;
    }

    /**
     * Retrieves a payload item.
     *
     * @param key - The key of the item.
     *
     * @returns - The item data or *None* otherwise.
     */
    public get(key: string): PayloadData | undefined {
        return this.contains(key) ? this._payload[key] : undefined;
    }

    /**
     * Checks if an item exists.
     *
     * @param key - The key of the item.
     */
    public contains(key: string): boolean {
        return !!this._payload[key];
    }

    /**
     * Removes an item or clears the entire payload.
     *
     * @param key - The key of the item; if set to *None*, all items will be removed.
     */
    public clear(key: string | undefined = undefined): void {
        if (!!key) {
            if (this.contains(key)) {
                delete this._payload[key];
            }
        } else {
            this._payload = {};
        }
    }

    /**
     * Encodes the payload for message passing.
     *
     * @returns - The encoded data.
     */
    public encode(): Payload {
        return this._payload;
    }

    /**
     * Decodes the payload from message passing.
     *
     * @param payload - The incoming payload.
     */
    public decode(payload: Payload): void {
        this._payload = payload;
    }

    public toString(): string {
        return JSON.stringify(this._payload);
    }
}
