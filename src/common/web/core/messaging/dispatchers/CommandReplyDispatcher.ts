import logging from "../../logging/Logging";
import { CommandReply } from "../CommandReply";
import { CommandReplyMetaInformation } from "../meta/CommandReplyMetaInformation";
import { CommandDispatcher } from "./CommandDispatcher";
import { MessageDispatcher } from "./MessageDispatcher";

/**
 * Message dispatcher specific to ``CommandReply``.
 */
export class CommandReplyDispatcher extends MessageDispatcher<CommandReply, CommandReplyMetaInformation> {
    /**
     * Called to perform tasks *before* sending a message.
     *
     * This method is called before any service-registered message handler is invoked.
     *
     * @param msg - The message that is about to be dispatched.
     * @param msgMeta - The message meta information.
     *
     * @throws Error - If the meta information type is invalid.
     */
    public preDispatch<MsgType extends CommandReply>(msg: MsgType, msgMeta: CommandReplyMetaInformation): void {
        logging.debug(`Dispatching command reply: ${String(msg)}`, "bus");
        super.preDispatch(msg, msgMeta);

        CommandDispatcher.invokeReplyCallbacks(msg.unique, msg, msgMeta);
        MessageDispatcher._metaInformationList.remove(msg.unique);
    }
}
