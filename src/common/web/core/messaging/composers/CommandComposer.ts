import { WebComponent } from "../../../component/WebComponent";
import { NetworkSettingIDs } from "../../../settings/NetworkSettingIDs";
import { ExecutionCallbacks } from "../../../utils/ExecutionCallbacks";
import { UnitID } from "../../../utils/UnitID";
import logging from "../../logging/Logging";
import { Command } from "../Command";
import { type CommandDoneCallback, type CommandFailCallback } from "../CommandReply";
import { type ConstructableMessage, Message } from "../Message";
import { type MessageBusProtocol } from "../MessageBusProtocol";
import { CommandMetaInformation } from "../meta/CommandMetaInformation";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";
import { MessageComposer } from "./MessageComposer";

/**
 * Composer for ``Command`` messages.
 */
export class CommandComposer<MsgType extends Command> extends MessageComposer<MsgType> {
    private _callbacks = new ExecutionCallbacks<CommandDoneCallback, CommandFailCallback>();

    private _timeout: number = 0.0;

    public constructor(
        originID: UnitID,
        messageBus: MessageBusProtocol,
        msgType: ConstructableMessage<MsgType>,
        params: Record<string, any> = {},
        chain: Message | null = null,
    ) {
        super(originID, messageBus, msgType, params, chain);

        this._timeout = WebComponent.instance.data.config.value<number>(NetworkSettingIDs.RegularCommandTimeout);
    }

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This composer instance to allow call chaining.
     */
    public done(cb: CommandDoneCallback): this {
        this._callbacks.done(cb);
        return this;
    }

    /**
     * Adds a *Fail* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This composer instance to allow call chaining.
     */
    public failed(cb: CommandFailCallback): this {
        this._callbacks.failed(cb);
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
        if (this._timeout > 0.0 && this._callbacks.failCallbacks.length == 0) {
            logging.warning(`Sending a command (${this._msgType}) with a timeout but no fail callback`, "bus");
        }
    }

    protected createMetaInformation(): MessageMetaInformation {
        return new CommandMetaInformation(MessageEntrypoint.Local, this._callbacks.doneCallbacks, this._callbacks.failCallbacks, this._timeout);
    }
}
