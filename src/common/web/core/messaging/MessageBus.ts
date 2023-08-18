import { ComponentData } from "../../component/ComponentData";
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
    private readonly _compData: ComponentData;

    private readonly _services: MessageService[] = [];
    private readonly _dispatchers: Record<MessageCategory, MessageDispatcher<any, any>> = {};
    private readonly _router: MessageRouter;

    /**
     * @param compData - The global component data.
     */
    public constructor(compData: ComponentData) {
        this._compData = compData;

        /*
        debug("-- Creating network engine", scope="bus")
        self._network_engine = self._create_network_engine()
         */

        this._dispatchers[Command.Category] = new CommandDispatcher();
        this._dispatchers[CommandReply.Category] = new CommandReplyDispatcher();
        this._dispatchers[Event.Category] = new EventDispatcher();

        this._router = new MessageRouter(compData.compID);
    }

    /**
     * Adds a new message service to the bus.
     *
     * @param svc - The message service to add.
     *
     * @returns - Whether the message service was added.
     */
    public addService(svc: MessageService): boolean {
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
    public removeService(svc: MessageService): boolean {
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
        // TODO:
        //self._network_engine.run()

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
        } catch (err) {
            logging.error(`A routing error occurred: ${String(err)}`, "bus", { message: msg });
            return;
        }

        if (this._router.checkRemoteRouting(msg, msgMeta)) {
            this.remoteDispatch(msg, msgMeta);
        }

        // The local dispatchers are always invoked for their pre- and post-steps
        this.localDispatch(msg, msgMeta);
    }

    private process(): void {
        // TODO:
        // self._network_engine.process()
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
                for (const svc of this._services) {
                    this.dispatchToService(dispatcher, msg, msgMeta, svc);
                }
            }
            dispatcher.postDispatch(msg, msgMeta);
        }
    }

    private remoteDispatch(msg: Message, msgMeta: MessageMetaInformation): void {
        // TODO
        // self._network_engine.send_message(msg, msg_meta)
    }

    private dispatchToService<DispatcherType extends MessageDispatcher<any, any>>(dispatcher: DispatcherType,
                                                                                  msg: Message, msgMeta: MessageMetaInformation,
                                                                                  svc: MessageService): void {
        for (const handler of svc.messageHandlers.findHandlers(msg.name)) {
            try {
                let ctx = this.createContext(msg, svc);
                dispatcher.dispatch(msg, msgMeta, handler, ctx);
            } catch (err) {
                logging.error(`An error occurred while processing a message: ${String(err)}`, "bus",
                    { message: String(msg), error: err });
            }
        }
    }

    private createContext(msg: Message, svc: MessageService): MessageContext {
        let logger = new LoggerProxy(logging.getDefaultLogger());
        logger.addParam("trace", String(msg.trace));
        return svc.createContext(logger, this._compData.config);
    }
}
