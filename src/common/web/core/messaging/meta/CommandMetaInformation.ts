import { MessageEntrypoint, MessageMetaInformation } from "./MessageMetaInformation";
import { type CommandDoneCallback, type CommandFailCallback } from "../CommandReply";

/**
 * Message meta information specific to ``Command``.
 */
export class CommandMetaInformation extends MessageMetaInformation {
    /**
     * @param entrypoint - From where the message entered the system (locally or remotely).
     * @param doneCallbacks - Called when a reply was received for this command.
     * @param failCallbacks - Called when no reply was received for this command or an exception occurred.
     * @param timeout - The timeout (in seconds) before a command is deemed not replied.
     */
    public constructor(readonly entrypoint: MessageEntrypoint,
                       readonly doneCallbacks: CommandDoneCallback[] = [],
                       readonly failCallbacks: CommandFailCallback[] = [],
                       readonly timeout: number = 0.0) {
        super(entrypoint, true);
    }
}
