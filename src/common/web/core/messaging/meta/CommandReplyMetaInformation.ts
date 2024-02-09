import { MessageMetaInformation } from "./MessageMetaInformation";

/**
 * Message meta information specific to ``CommandReply``.
 */
export class CommandReplyMetaInformation extends MessageMetaInformation {
    private _isHandledExternally: boolean = false;

    /**
     * Whether the message is handled outside the message bus.
     */
    public get isHandledExternally(): boolean {
        return this._isHandledExternally;
    }

    /**
     * Sets whether the message is handled outside the message bus.
     */
    public set isHandledExternally(handled: boolean) {
        this._isHandledExternally = handled;
    }
}
