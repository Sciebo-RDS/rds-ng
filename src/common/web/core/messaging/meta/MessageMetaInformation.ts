/**
 * Defines from where a message has entered the system.
 */
export enum MessageEntrypoint {
    Local,
    Server
}

/**
 * Stores additional information necessary for message dispatching.
 *
 * When a message is emitted, additional information is required to be able to properly handle it.
 * This includes its entrypoint into the system, as well as whether the message type requires a reply.
 */
export class MessageMetaInformation {
    /**
     * @param entrypoint - From where the message entered the system (locally or remotely).
     * @param requiresReply - Whether a reply is expected.
     */
    public constructor(readonly entrypoint: MessageEntrypoint, readonly requiresReply: boolean = false) {
    }
}
