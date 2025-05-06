import { Logger } from "./Logger";
import { LogLevel } from "./LogRecord";

const defaultLogger = new Logger();

/**
 * Sets the default log level.
 *
 * @param level - The maximum level for log entries to be displayed.
 */
export function setLevel(level: LogLevel): void {
    defaultLogger.setLevel(level);
}

/**
 * Logs a debugging message.
 *
 * @param msg - The text to log.
 * @param scope - The scope of the entry.
 * @param params - Any additional parameters.
 */
export function debug(msg: string, scope: string = "", params: Record<string, any> = {}): void {
    defaultLogger.debug(msg, scope, params);
}

/**
 * Logs an info message.
 *
 * @param msg - The text to log.
 * @param scope - The scope of the entry.
 * @param params - Any additional parameters.
 */
export function info(msg: string, scope: string = "", params: Record<string, any> = {}): void {
    defaultLogger.info(msg, scope, params);
}

/**
 * Logs a warning message.
 *
 * @param msg - The text to log.
 * @param scope - The scope of the entry.
 * @param params - Any additional parameters.
 */
export function warning(msg: string, scope: string = "", params: Record<string, any> = {}): void {
    defaultLogger.warning(msg, scope, params);
}

/**
 * Logs an error message.
 *
 * @param msg - The text to log.
 * @param scope - The scope of the entry.
 * @param params - Any additional parameters.
 */
export function error(msg: string, scope: string = "", params: Record<string, any> = {}): void {
    defaultLogger.error(msg, scope, params);
}

/**
 * Retrieves the global default logger.
 */
export function getDefaultLogger(): Logger {
    return defaultLogger;
}

export default { setLevel, debug, info, warning, error, getDefaultLogger };
