import { ComponentData } from "../component/ComponentData";
import { GeneralSettingIDs } from "../settings/GeneralSettingIDs";
import logging from "../core/logging/Logging"
import { LogLevel } from "./logging/LogRecord";

/*
@Message.define("sum/tssst")
class X extends Command {
    public value: int = 12;
}

 */

/**
 * The main *underlying basis* of any component.
 *
 * The ``Core`` brings together all portions and aspects that build the underlying foundation of every web component,
 * including the ``MessageBus``.
 *
 * The core can be regarded as a facade to the *inner structure* of a component. It only offers a small number of public
 * methods and is accessed from the outside very rarely.
 *
 * An instance of this class is always created when creating a ``Component``; it should never be instantiated otherwise.
 */
export class Core {
    private readonly _compData: ComponentData;

    /**
     *
     * @param compData - The component data used to access common component information.
     */
    public constructor(compData: ComponentData) {
        logging.info("Initializing core...", "core")

        this._compData = compData;

        if (this.isDebugMode) {
            this.enableDebugMode();
        }
        /*
                let x = new X(new UnitID("me", "unit"), new UnitID("me", "unit"), Channel.direct("hans/kanns/nicht"),
                    [new UnitID("hoop", "de", "loop")]);
                console.log(x.name);
                console.log(x.convertToJSON())
         */
    }

    private enableDebugMode(): void {
        logging.setLevel(LogLevel.Debug);
        logging.debug("-- Debug mode enabled", "core")
    }

    /**
     * Whether we're running in Debug mode.
     */
    public get isDebugMode(): boolean {
        return this._compData.config.value(GeneralSettingIDs.Debug);
    }
}
