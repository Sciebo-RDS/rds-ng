// @ts-ignore
import { v4 as uuidv4 } from "uuid";

import { Message, type MessageCategory, type Trace } from "./Message";

/**
 * Used when a command failed.
 */
export const enum CommandFailType {
    None = 0,
    Timeout,
    Exception,
    Unknown,
}

/**
 * A command reply message.
 *
 * Every command needs to receive a reply in the form of a ``CommandReply`` message. The reply contains
 * information about its ``success``, as well as a text message which is usually used to describe reasons for
 * failures.
 */
export class CommandReply extends Message {
    public static readonly Category: MessageCategory = "CommandReply";

    public readonly success: boolean = true;
    public readonly message: string = "";

    public readonly unique: Trace = uuidv4();

    /**
     * Gets the global message category.
     */
    public get messageCategory(): MessageCategory {
        return CommandReply.Category;
    }
}

export type CommandDoneCallback = (reply: CommandReply, success: boolean, msg: string) => void;
export type CommandFailCallback = (failType: CommandFailType, msg: string) => void;
