import { LoggerProxy } from "../core/logging/LoggerProxy";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { MessageContext } from "../core/messaging/handlers/MessageContext";
import { MessageMetaInformation } from "../core/messaging/meta/MessageMetaInformation";
import { Configuration } from "../utils/config/Configuration";

/**
 * An execution context for messages dispatched by the message bus to a service.
 *
 * This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.
 */
export class ServiceContext extends MessageContext {
    private readonly _config: Configuration;

    /**
     * @param msgMeta - The meta information of the message.
     * @param msgBuilder - A ``MessageBuilder`` to be assigned to this context.
     * @param logger - A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
     * @param config - The global component configuration.
     */
    public constructor(msgMeta: MessageMetaInformation, msgBuilder: MessageBuilder, logger: LoggerProxy, config: Configuration) {
        super(msgMeta, msgBuilder, logger);

        this._config = config;
    }

    /**
     * The global component configuration.
     */
    public get config(): Configuration {
        return this._config;
    }
}
