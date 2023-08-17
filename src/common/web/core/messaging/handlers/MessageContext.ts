import { MessageEmitter, MessageEmitterCounter } from "./MessageEmitter";
import { LoggerProxy } from "../../logging/LoggerProxy";

/**
 * An execution context for messages dispatched by the message bus.
 *
 * When a message handler gets executed (i.e., called by the message bus dispatchers), an instance of ``MessageContext`` (or a subclass)
 * is passed to the handler. This context can be seen as a *unit of work* that exists during the execution of the handler. Its main task is to
 * hold data that is specific to this single execution.
 *
 * A message context is used as a context manager. In its ``__exit__`` method, any exceptions will be catched, printed and passed on. This
 * makes tracing of errors that occur during message handling easier.
 *
 * It is also possible to have message handlers receive custom subtypes of this class. See ``Component`` and its ``create_service`` method for
 * details.
 */
export class MessageContext {
    private readonly _msgEmitter: MessageEmitter;

    private readonly _logger: LoggerProxy;

    private _requiresReply: boolean = false;

    /**
     * @param msgEmitter - A ``MessageEmitter`` to be assigned to this context.
     * @param logger - A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
     */
    public constructor(msgEmitter: MessageEmitter, logger: LoggerProxy) {
        this._msgEmitter = msgEmitter;

        this._logger = logger;
    }

    /**
     * Initiates execution within this context.
     *
     * @param requiresReply - Whether a reply is required.
     */
    public begin(requiresReply: boolean): void {
        this._requiresReply = requiresReply;
    }

    /**
     * Finishes execution within this context.
     */
    public end(): void {
        this.checkCommandReply();
    }

    /**
     * Reports an error occurred during context execution.
     *
     * @param err - The error to report.
     */
    public reportError(err: any): void {
        this._logger.error(`An error occurred within a message context: ${String(err)}`, "bus", { error: err });
    }

    private checkCommandReply(): void {
        if (this._requiresReply && this._msgEmitter.getMessageCount(MessageEmitterCounter.CommandReply) == 0) {
            this._logger.warning("A message context required a command reply, but none was sent", "bus");
        }
    }

    /**
     * The message emitter to be used within this context.
     */
    public get messageEmitter(): MessageEmitter {
        return this._msgEmitter;
    }

    /**
     * The logger to be used within this context.
     */
    public get loggger(): LoggerProxy {
        return this._logger;
    }
}
