import logging from "../../logging/Logging";
import { Command } from "../Command";
import { type CommandDoneCallback, type CommandFailCallback } from "../CommandReply";
import { CommandMetaInformation } from "../meta/CommandMetaInformation";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";
import { MessageComposer } from "./MessageComposer";

/**
 * Composer for ``Command`` messages.
 */
export class CommandComposer<MsgType extends Command> extends MessageComposer<MsgType> {
    private _doneCallback: CommandDoneCallback | null = null;
    private _failCallback: CommandFailCallback | null = null;
    private _timeout: number = 0.0;

    /**
     * Assigns a *Done* callback.
     *
     * @param cb - The callback to use.
     *
     * @returns - This composer instance to allow call chaining.
     */
    public done(cb: CommandDoneCallback | null): this {
        this._doneCallback = cb;
        return this;
    }

    /**
     * Assigns a *Fail* callback.
     *
     * @param cb - The callback to use.
     *
     * @returns - This composer instance to allow call chaining.
     */
    public failed(cb: CommandDoneCallback | null): this {
        this._failCallback = cb;
        return this;
    }

    /**
     * Assigns a *Done* callback.
     *
     * @param timeout - The timeout (in seconds).
     *
     * @returns - This composer instance to allow call chaining.
     */
    public timeout(timeout: number): this {
        this._timeout = timeout;
        return this;
    }

    protected verify(): void {
        if (this._timeout > 0.0 && !this._failCallback) {
            logging.warning(`Sending a command (${this._msgType}) with a timeout but no fail callback`, "bus");
        }
    }

    protected createMetaInformation(): MessageMetaInformation {
        return new CommandMetaInformation(MessageEntrypoint.Local, this._doneCallback, this._failCallback, this._timeout);
    }
}
