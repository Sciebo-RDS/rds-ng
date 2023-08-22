import { LoggerProxy } from "../core/logging/LoggerProxy";
import { MessageContext } from "../core/messaging/handlers/MessageContext";
import { MessageEmitter } from "../core/messaging/handlers/MessageEmitter";
import { Configuration } from "../utils/config/Configuration";

/**
 * An execution context for messages dispatched by the message bus to a service.
 *
 * This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.
 */
export class ServiceContext extends MessageContext {
    private readonly _config: Configuration;

    /**
     * @param msgEmitter - A ``MessageEmitter`` to be assigned to this context.
     * @param logger - A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
     * @param config - The global component configuration.
     */
    public constructor(msgEmitter: MessageEmitter, logger: LoggerProxy, config: Configuration) {
        super(msgEmitter, logger);

        this._config = config;
    }

    /**
     * The global component configuration.
     */
    public get config(): Configuration {
        return this._config;
    }
}
