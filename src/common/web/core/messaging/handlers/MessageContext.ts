import { Configuration } from "../../../utils/config/Configuration";
import { UnitID } from "../../../utils/UnitID";
import { LoggerProxy } from "../../logging/LoggerProxy";
import { MessageBuilder } from "../composers/MessageBuilder";
import { CommandReply } from "../CommandReply";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";

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
 * It is also possible to have message handlers receive custom subtypes of this class. See ``WebComponent`` and its ``create_service`` method for
 * details.
 */
export class MessageContext {
    protected readonly _msgMeta: MessageMetaInformation;
    protected readonly _msgOrigin: UnitID;
    protected readonly _msgBuilder: MessageBuilder;

    protected readonly _logger: LoggerProxy;
    protected readonly _config: Configuration;

    protected _requiresReply: boolean = false;

    /**
     * @param msgMeta - The meta information of the message.
     * @param msgOrigin - The origin of the message.
     * @param msgBuilder - A ``MessageBuilder`` to be assigned to this context.
     * @param logger - A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
     * @param config - The global component configuration.
     */
    public constructor(msgMeta: MessageMetaInformation, msgOrigin: UnitID, msgBuilder: MessageBuilder, logger: LoggerProxy, config: Configuration) {
        this._msgMeta = msgMeta;
        this._msgOrigin = msgOrigin;
        this._msgBuilder = msgBuilder;

        this._logger = logger;
        this._config = config;
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
        if (this._requiresReply && this._msgBuilder.getMessageCount(CommandReply.Category) != 1) {
            this._logger.warning("A message context required exactly one command reply, but either none or more than one was sent", "bus");
        }
    }

    /**
     * Whether the message entered locally.
     */
    public get isEntrypointLocal(): boolean {
        return this._msgMeta.entrypoint == MessageEntrypoint.Local;
    }

    /**
     * Whether the message entered through the server.
     */
    public get isEntrypointServer(): boolean {
        return this._msgMeta.entrypoint == MessageEntrypoint.Server;
    }

    /**
     * Whether the message entered through the client.
     */
    public get isEntrypointClient(): boolean {
        return this._msgMeta.entrypoint == MessageEntrypoint.Client;
    }

    /**
     * The origin of the message.
     */
    public get origin(): UnitID {
        return this._msgOrigin;
    }

    /**
     * The message builder to be used within this context.
     */
    public get messageBuilder(): MessageBuilder {
        return this._msgBuilder;
    }

    /**
     * The logger to be used within this context.
     */
    public get logger(): LoggerProxy {
        return this._logger;
    }

    /**
     * The global component configuration.
     */
    public get config(): Configuration {
        return this._config;
    }
}
