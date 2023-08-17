/**
 * Defines the general interface for our extended ``Logger``.
 */
export interface LoggerProtocol {
    debug(msg: string, scope: string, params: Record<string, any>): void;

    info(msg: string, scope: string, params: Record<string, any>): void;

    warning(msg: string, scope: string, params: Record<string, any>): void;

    error(msg: string, scope: string, params: Record<string, any>): void;
}
