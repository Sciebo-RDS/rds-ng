import { UnitID } from "../../../utils/UnitID";
import { Channel } from "../Channel";
import { Command } from "../Command";
import { CommandReply } from "../CommandReply";
import { type ConstructableMessage } from "../Message";
import { type MessageBusProtocol } from "../MessageBusProtocol";
import { CommandReplyMetaInformation } from "../meta/CommandReplyMetaInformation";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";
import { MessageComposer } from "./MessageComposer";

/**
 * Composer for ``CommandReply`` messages.
 */
export class CommandReplyComposer<MsgType extends CommandReply> extends MessageComposer<MsgType> {
    private readonly _command: Command;

    public constructor(originID: UnitID, messageBus: MessageBusProtocol, msgType: ConstructableMessage<MsgType>, cmd: Command,
                       params: Record<string, any> = {}) {
        super(originID, messageBus, msgType, params, cmd);

        this._command = cmd;
    }

    /**
     * Sends the built message through the message bus.
     */
    public emit(): void {
        let target = this._command.origin.equals(this._originID) ? Channel.local() : Channel.direct(this._command.origin.toString());
        super.emit(target);
    }

    protected createMetaInformation(): MessageMetaInformation {
        return new CommandReplyMetaInformation(MessageEntrypoint.Local);
    }
}
