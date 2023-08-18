import { Logger } from "./Logger";

/**
 * A proxy to automatically pass extra parameters to a logger.
 *
 * This class allows us to store additional, fixed parameters passed to an existing logger, avoiding the need to use
 * a new logger instance. It offers the same public interface as an actual ``Logger`` and can thus be used like a
 * *real* logger.
 */
export class LoggerProxy {
    private readonly _logger: Logger;

    private _autoParams: Record<string, any> = {};

    /**
     * @param logger - The logger to use.
     */
    public constructor(logger: Logger) {
        this._logger = logger;
    }

    /**
     * Adds a new paramter that is always automatically passed to the logger.
     *
     * @param name - The name of the parameter.
     * @param value - Its value.
     */
    public addParam(name: string, value: any): void {
        this._autoParams[name] = value;
    }

    /**
     * Removes a parameter that has been added previously.
     *
     * @param name - The name of the parameter.
     */
    public removeParam(name: string): void {
        delete this._autoParams[name];
    }

    /**
     * Removes all stored parameters.
     */
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
    public debug(msg: string, scope: string = "", params: Record<string, any> = {}): void {
        this._logger.debug(msg, scope, { ...this._autoParams, ...params });
    }

    /**
     * Logs an info message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public info(msg: string, scope: string = "", params: Record<string, any> = {}): void {
        this._logger.info(msg, scope, { ...this._autoParams, ...params });
    }

    /**
     * Logs a warning message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public warning(msg: string, scope: string = "", params: Record<string, any> = {}): void {
        this._logger.warning(msg, scope, { ...this._autoParams, ...params });
    }

    /**
     * Logs an error message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public error(msg: string, scope: string = "", params: Record<string, any> = {}): void {
        this._logger.error(msg, scope, { ...this._autoParams, ...params });
    }
}
