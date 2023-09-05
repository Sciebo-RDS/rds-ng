import { WebComponentData } from "../../component/WebComponentData";
import { LoggerProxy } from "../logging/LoggerProxy";
import logging from "../logging/Logging";
import { Command } from "./Command";
import { CommandReply } from "./CommandReply";
import { CommandDispatcher } from "./dispatchers/CommandDispatcher";
import { CommandReplyDispatcher } from "./dispatchers/CommandReplyDispatcher";
import { EventDispatcher } from "./dispatchers/EventDispatcher";
import { MessageDispatcher } from "./dispatchers/MessageDispatcher";
import { Event } from "./Event";
import { MessageContext } from "./handlers/MessageContext";
import { MessageService } from "./handlers/MessageService";
import { Message, type MessageCategory } from "./Message";
import { MessageRouter } from "./MessageRouter";
import { MessageMetaInformation } from "./meta/MessageMetaInformation";
import { NetworkEngine } from "./networking/NetworkEngine";

/**
 * Bus for dispatching messages.
 *
 * The message bus is probably the most central aspect of the system as a whole. It not only invokes local message handlers (which are basically
 * callback functions), it also sends messages across the network to other components if necessary. The message bus on the remote side will then
 * decide what to do with the incoming message: Dispatch it locally there, send it to yet another component, or just ignore it.
 *
 * Message handlers are always registered through a ``MessageService``. When a message gets dispatched locally by the bus, it will call any handlers
 * associated with the message (via its name). If a message needs to be sent to another component, the bus will invoke the ``NetworkEngine`` to do
 * so.
 *
 * To be error tolerant, any exceptions that arise during message handling will be logged but won't result in program termination.
 */
export class MessageBus {
    private readonly _compData: WebComponentData;

    private readonly _networkEngine: NetworkEngine;
    private readonly _services: MessageService<any>[] = [];
    private readonly _dispatchers: Record<MessageCategory, MessageDispatcher<any, any>> = {};
    private readonly _router: MessageRouter;

    /**
     * @param compData - The global component data.
     */
    public constructor(compData: WebComponentData) {
        this._compData = compData;

        logging.debug("-- Creating network engine", "bus")
        this._networkEngine = this.createNetworkEngine();

        this._dispatchers[Command.Category] = new CommandDispatcher();
        this._dispatchers[CommandReply.Category] = new CommandReplyDispatcher();
        this._dispatchers[Event.Category] = new EventDispatcher();

        this._router = new MessageRouter(compData.compID);
    }

    private createNetworkEngine(): NetworkEngine {
        return new NetworkEngine(this._compData, this);
    }

    /**
     * Adds a new message service to the bus.
     *
     * @param svc - The message service to add.
     *
     * @returns - Whether the message service was added.
     */
    public addService<CtxType extends MessageContext>(svc: MessageService<CtxType>): boolean {
        if (this._services.indexOf(svc) != -1) {
            return false;
        }

        this._services.push(svc);
        return true;
    }

    /**
     * Removes a message service from the bus.
     *
     * @param svc - svc: The message service to remove.
     *
     * @returns - Whether the message service was removed.
     */
    public removeService<CtxType extends MessageContext>(svc: MessageService<CtxType>): boolean {
        let index = this._services.indexOf(svc);
        if (index == -1) {
            return false;
        }

        this._services.splice(index, 1);
        return true;
    }

    /**
     * Initiates periodic tasks performed by the bus.
     */
    public run(): void {
        this._networkEngine.run();

        setInterval(() => this.process(), 1000);
    }

    /**
     * Dispatches a message.
     *
     * To do so, the message is first checked for validity (whether it actually *may* be dispatched). If it is valid,
     * the ``MessageRouter`` will determine if it needs to be dispatched to another component or locally (or both).
     *
     * @param msg - The message to be dispatched.
     * @param msgMeta - The message meta information.
     */
    public dispatch(msg: Message, msgMeta: MessageMetaInformation): void {
        try {
            this._router.verifyMessage(msg, msgMeta);

            if (this._router.checkRemoteRouting(msg, msgMeta)) {
                this.remoteDispatch(msg, msgMeta);
            }

            // The local dispatchers are always invoked for their pre- and post-steps
            this.localDispatch(msg, msgMeta);
        } catch (err) {
            logging.error(`A routing error occurred: ${String(err)}`, "bus", { message: msg });
        }
    }

    private process(): void {
        this._networkEngine.process();

        for (const [_, dispatcher] of Object.entries(this._dispatchers)) {
            dispatcher.process();
        }
    }

    private localDispatch(msg: Message, msgMeta: MessageMetaInformation): void {
        let localRouting = this._router.checkLocalRouting(msg, msgMeta);
        for (const [category, dispatcher] of Object.entries(this._dispatchers)) {
            if (msg.category != category) {
                continue;
            }

            dispatcher.preDispatch(msg, msgMeta);

            if (localRouting) {
                let msgDispatched = false;
                for (const svc of this._services) {
                    msgDispatched |= this.dispatchToService(dispatcher, msg, msgMeta, svc);
                }

                if (!msgDispatched) {
                    logging.warning("A message was dispatched locally but not handled", "bus", { message: msg });
                }
            }

            dispatcher.postDispatch(msg, msgMeta);
        }
    }

    private remoteDispatch(msg: Message, msgMeta: MessageMetaInformation): void {
        this._networkEngine.sendMessage(msg, msgMeta);
    }

    private dispatchToService<DispatcherType extends MessageDispatcher<any, any>,
        CtxType extends MessageContext>(dispatcher: DispatcherType,
                                        msg: Message, msgMeta: MessageMetaInformation,
                                        svc: MessageService<CtxType>): boolean {
        let msgDispatched = false;
        for (const handler of svc.messageHandlers.findHandlers(msg.name)) {
            try {
                let ctx = this.createContext<CtxType>(msg, msgMeta, svc);
                dispatcher.dispatch(msg, msgMeta, handler, ctx);
                msgDispatched = true;
            } catch (err) {
                logging.error(`An error occurred while processing a message: ${String(err)}`, "bus",
                    { message: msg, error: err });
            }
        }

        return msgDispatched;
    }

    private createContext<CtxType extends MessageContext>(msg: Message, msgMeta: MessageMetaInformation, svc: MessageService<CtxType>): MessageContext {
        let logger = new LoggerProxy(logging.getDefaultLogger());
        logger.addParam("trace", msg.trace);
        return svc.createContext(msgMeta, logger, this._compData.config);
    }
}
