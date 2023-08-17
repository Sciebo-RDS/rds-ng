import { UnitID } from "../../../utils/UnitID";
import { MessageHandlers } from "./MessageHandlers";
import { Constructable } from "../../../utils/Types";
import { MessageContext } from "./MessageContext";
import { LoggerProtocol } from "../../logging/LoggerProtocol";
import { MessageEmitter } from "./MessageEmitter";

/**
 * Base class for all message services.
 *
 * A *message service* wraps message handlers and proper message context creation (i.e., using a flexible context type). It
 * is used by the message bus as an encapsulated layer for message dispatching.
 */
export class MessageService<T extends MessageContext = MessageContext> {
    private readonly _compID: UnitID;

    // TODO: MsgBus
    private readonly _msgHandlers: MessageHandlers;
    private readonly _contextType: Constructable<T>;

    /**
     * @param compID - The global component identifier.
     * @param contextType - The type to use when creating a message context.
     */
    public constructor(compID: UnitID, /*bus*/ contextType: Constructable<T> = MessageContext) {
        this._compID = compID;

        this._msgHandlers = new MessageHandlers();
        this._contextType = contextType;
    }

    /**
     * Creates a new service context.
     *
     * @param logger - The logger to be used within the new context.
     * @param args - Any additional parameters.
     *
     * @returns - The newly created message context.
     */
    public createContext(logger: LoggerProtocol, ...args: any[]): MessageContext {
        return new this._contextType(this.createMessageEmitter(), logger, ...args);
    }

    /**
     * Creates a new message emitter.
     *
     * @returns - The newly created message emitter.
     */
    public createMessageEmitter(): MessageEmitter {
        return new MessageEmitter(this._compID);  // TODO: MsgBus
    }

    /**
     * The message handlers maintained by this message service.
     */
    public get messageHandlers(): MessageHandlers {
        return this._msgHandlers;
    }
}
