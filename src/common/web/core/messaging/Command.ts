import { Message, type Trace } from "./Message";

// @ts-ignore
import { v4 as uuidv4 } from "uuid";

/**
 * A command message.
 *
 * Commands are instructions that need to be *executed* by the receiving component.
 *
 * Notes:
 *     Commands need to *always* be replied by emitting a corresponding ``CommandReply``.
 *     This reply is then automatically sent back to the original sender.
 */
export class Command extends Message {
    public readonly unique: Trace = uuidv4();
}
