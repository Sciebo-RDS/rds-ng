import { UnitID } from "../../utils/UnitID";

/**
 * The different channel types.
 */
export const enum ChannelType {
    Local = "local",
    Direct = "direct"
}

/**
 * The target of a message.
 *
 * Message targets are represented by so-called *channels*. These can be *local* for messages that will only
 * be dispatched locally and not across the network or *direct* for specific (remote) targets.
 */
export class Channel {
    /**
     * @param type - The channel type.
     * @param target - The actual target in case of a direct channel.
     */
    public constructor(readonly type: string, readonly target?: string) {
    }

    /**
     * Generates a ``UnitID`` from the target of this channel.
     *
     * @returns - The component ID of the target, if any.
     */
    public get targetID(): UnitID | null {
        try {
            return this.target ? UnitID.fromString(this.target) : null;
        } catch {
            return null;
        }
    }

    /**
     * Whether this is a local channel.
     */
    public get isLocal(): boolean {
        return this.type == ChannelType.Local;
    }

    /**
     * Whether this is a direct channel.
     */
    public get isDirect(): boolean {
        return this.type == ChannelType.Direct;
    }

    /**
     * Gets the string representation of this channel.
     */
    public toString(): string {
        return this.target ? `@${this.type}:${this.target}` : `@${this.type}`;
    }

    /**
     * Creates a new local channel.
     */
    public static local(): Channel {
        return new Channel(ChannelType.Local);
    }

    /**
     * Creates a new direct channel.
     */
    public static direct(target: string | UnitID) {
        return new Channel(ChannelType.Direct, String(target));
    }
}
