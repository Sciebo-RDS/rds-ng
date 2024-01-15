import { WebComponentData } from "../component/WebComponentData";
import logging from "../core/logging/Logging";
import { GeneralSettingIDs } from "../settings/GeneralSettingIDs";
import { LogLevel } from "./logging/LogRecord";
import { MessageService } from "./messaging/handlers/MessageService";
import { MessageBus } from "./messaging/MessageBus";

/**
 * The main *underlying basis* of any component.
 *
 * The ``Core`` brings together all portions and aspects that build the underlying foundation of every web component,
 * including the ``MessageBus``.
 *
 * The core can be regarded as a facade to the *inner structure* of a component. It only offers a small number of public
 * methods and is accessed from the outside very rarely.
 *
 * An instance of this class is always created when creating a ``WebComponent``; it should never be instantiated otherwise.
 */
export class Core {
    private readonly _compData: WebComponentData;

    private readonly _messageBus: MessageBus;

    /**
     * @param compData - The component data used to access common component information.
     */
    public constructor(compData: WebComponentData) {
        logging.info("Initializing core", "core");

        this._compData = compData;

        if (this.isDebugMode) {
            this.enableDebugMode();
        }

        logging.debug("Creating message bus", "core");
        this._messageBus = this.createMessageBus();
    }

    private enableDebugMode(): void {
        logging.setLevel(LogLevel.Debug);
        logging.debug("Debug mode enabled", "core");
    }

    private createMessageBus(): MessageBus {
        return new MessageBus(this._compData);
    }

    /**
     * Registers a message service.
     *
     * Services are always created and registered using ``create_service`` (in ``WebComponent``),
     * so you should rarely (if ever) need to call this method directly.
     *
     * @param svc - The message service to register.
     */
    public registerService(svc: MessageService): void {
        if (this._messageBus.addService(svc)) {
            logging.debug(`Registered service: ${svc}`, "core");
        } else {
            logging.debug(`Service already registered: ${svc}`, "core", { service: svc });
        }
    }

    /**
     * Removes a message service.
     *
     * @param svc - The message service to remove.
     */
    public unregisterService(svc: MessageService): void {
        if (this._messageBus.removeService(svc)) {
            logging.debug(`Unregistered service: ${svc}`, "core");
        } else {
            logging.debug(`Service not registered: ${svc}`, "core", { service: svc });
        }
    }

    /**
     * Starts periodic background tasks.
     */
    public run(): void {
        this._messageBus.run();
    }

    /**
     * The global ``MessageBus`` instance.
     */
    public get messageBus(): MessageBus {
        return this._messageBus;
    }

    /**
     * Whether we're running in Debug mode.
     */
    public get isDebugMode(): boolean {
        return this._compData.config.value<boolean>(GeneralSettingIDs.Debug);
    }
}
