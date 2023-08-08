import { Logger } from "./Logger";
import { LogRecordParameters } from "./LogRecord";

export class LoggerProxy {
    private readonly _logger: Logger;

    private _autoParams: LogRecordParameters = {};

    public constructor(logger: Logger) {
        this._logger = logger;
    }

    public addParam(name: string, value: any): void {
        this._autoParams[name] = value;
    }

    public removeParam(name: string): void {
        delete this._autoParams[name];
    }

    public clearParams(): void {
        this._autoParams = {};
    }

    /**
     * Logs a debugging message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public debug(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        this._logger.debug(msg, scope, { ...this._autoParams, ...params });
    }

    /**
     * Logs an info message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public info(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        this._logger.info(msg, scope, { ...this._autoParams, ...params });
    }

    /**
     * Logs a warning message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public warning(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        this._logger.warning(msg, scope, { ...this._autoParams, ...params });
    }

    /**
     * Logs an error message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public error(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        this._logger.error(msg, scope, { ...this._autoParams, ...params });
    }
}
