import { Configuration } from "../../../utils/config/Configuration";
import { type Constructable } from "../../../utils/Types";
import { UnitID } from "../../../utils/UnitID";
import { LoggerProxy } from "../../logging/LoggerProxy";
import { MessageBuilder } from "../composers/MessageBuilder";
import { type MessageBusProtocol } from "../MessageBusProtocol";
import { MessageMetaInformation } from "../meta/MessageMetaInformation";
import { MessageContext } from "./MessageContext";
import { MessageHandlers } from "./MessageHandlers";

/**
 * Base class for all message services.
 *
 * A *message service* wraps message handlers and proper message context creation (i.e., using a flexible context type). It
 * is used by the message bus as an encapsulated layer for message dispatching.
 */
export class MessageService<CtxType extends MessageContext = MessageContext> {
    private readonly _compID: UnitID;

    private readonly _messageBus: MessageBusProtocol;
    private readonly _messageHandlers: MessageHandlers;
    private readonly _contextType: Constructable<CtxType>;

    /**
     * @param compID - The global component identifier.
     * @param messageBus - The global message bus.
     * @param contextType - The type to use when creating a message context.
     */
    public constructor(compID: UnitID, messageBus: MessageBusProtocol, contextType: Constructable<CtxType> = MessageContext as Constructable<CtxType>) {
        this._compID = compID;

        this._messageBus = messageBus;
        this._messageHandlers = new MessageHandlers();
        this._contextType = contextType;
    }

    /**
     * Creates a new service context.
     *
     * @param msgMeta - The meta information of the message.
     * @param logger - The logger to be used within the new context.
     * @param config - The global component configuration.
     *
     * @returns - The newly created message context.
     */
    public createContext(msgMeta: MessageMetaInformation, logger: LoggerProxy, config: Configuration): MessageContext {
        return new this._contextType(msgMeta, this.createMessageBuilder(), logger, config);
    }

    /**
     * Creates a new message builder.
     *
     * @returns - The newly created message builder.
     */
    public createMessageBuilder(): MessageBuilder {
        return new MessageBuilder(this._compID, this._messageBus);
    }

    /**
     * The message handlers maintained by this message service.
     */
    public get messageHandlers(): MessageHandlers {
        return this._messageHandlers;
    }
}
