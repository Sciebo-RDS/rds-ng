import logging from "../../logging/Logging";
import { Command } from "../Command";
import { CommandFailType, CommandReply } from "../CommandReply";
import { MessageContext } from "../handlers/MessageContext";
import { MessageHandlerMapping } from "../handlers/MessageHandler";
import { type Trace } from "../Message";
import { CommandMetaInformation } from "../meta/CommandMetaInformation";
import { MessageDispatcher } from "./MessageDispatcher";

/**
 * Message dispatcher specific to ``Command``.
 */
export class CommandDispatcher extends MessageDispatcher<Command, CommandMetaInformation> {
    /**
     * Takes care of checking whether issued commands have already timed out.
     */
    public process(): void {
        super.process();

        for (const unique of MessageDispatcher._metaInformationList.findTimedOutEntries()) {
            CommandDispatcher.invokeReplyCallback(unique, null, CommandFailType.Timeout, "The command timed out");
            MessageDispatcher._metaInformationList.remove(unique);
        }
    }

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
    public preDispatch(msg: Command, msgMeta: CommandMetaInformation): void {
        super.preDispatch(msg, msgMeta);

        MessageDispatcher._metaInformationList.add(msg.unique, msgMeta, msgMeta.timeout);
    }

    /**
     * Dispatches a message to locally registered message handlers.
     *
     * Notes:
     *     Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.
     *
     * @param msg - The message to be dispatched.
     * @param msgMeta - The message meta information.
     * @param handler - The handler to be invoked.
     * @param ctx - The message context.
     *
     * @throws Error - If the handler requires a different message type.
     */
    public dispatch<CtxType extends MessageContext>(msg: Command, msgMeta: CommandMetaInformation, handler: MessageHandlerMapping, ctx: CtxType): void {
        ctx.logger.debug(`Dispatching command: ${String(msg)}`, "bus");
        super.dispatch(msg, msgMeta, handler, ctx);
    }

    protected contextError(err: any, msg: Command, msgMeta: CommandMetaInformation): void {
        CommandDispatcher.invokeReplyCallback(msg.unique, null, CommandFailType.Exception, String(err));
        MessageDispatcher._metaInformationList.remove(msg.unique);
    }

    /**
     * Invokes command reply handlers.
     *
     *  When emitting a command, it is possible to specify reply callbacks that are invoked beside message handlers. This method will call the correct
     *  callback and take care of intercepting exceptions.
     *
     * @param unique - The unique trace of the command.
     * @param reply - The received command reply (if any).
     * @param failType - The type of the command failure (in case of a timeout or exception).
     * @param failMsg - The failure message.
     */
    public static invokeReplyCallback(unique: Trace, reply: CommandReply | null = null,
                                      failType: CommandFailType = CommandFailType.None, failMsg: string = ""): void {
        let invoke = (callback?: Function, ...args: any[]): void => {
            if (callback) {
                try {
                    callback(...args);
                } catch (err) {
                    logging.error(`An error occurred within a command reply callback: ${String(err)}`, "bus", { error: typeof err });
                }
            }
        }

        let metaInfo = MessageDispatcher._metaInformationList.find(unique);
        if (metaInfo !== null && metaInfo instanceof CommandMetaInformation) {
            if (reply !== null) {
                invoke(metaInfo.doneCallback, reply, reply.success, reply.message);
            } else {
                invoke(metaInfo.failCallback, failType, failMsg);
            }
        }
    }
}
