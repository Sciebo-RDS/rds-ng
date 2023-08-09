import { Formatter } from "./Formatter";
import { LogLevel, LogRecord, type LogRecordParameters } from "./LogRecord";

/**
 * A customized logger offering advanced formatting and parameters listing.
 *
 * This logger and its corresponding ``Formatter`` display the log level, scope, as well as a parameters listing
 * in a color-rich format for easy readability.
 */
export class Logger {
    private _level: LogLevel;

    /**
     * @param level - The maximum level for log entries to be displayed.
     */
    public constructor(level: LogLevel = LogLevel.Info) {
        this._level = level;
    }

    /**
     * Sets the maximum logging level.
     *
     * @param level - The logging level.
     */
    public setLevel(level: LogLevel): void {
        this._level = level;
    }

    /**
     * Logs a debugging message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public debug(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        let record = this.createLogRecord(LogLevel.Debug, msg, scope, params);
        this.log(record);
    }

    /**
     * Logs an info message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public info(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        let record = this.createLogRecord(LogLevel.Info, msg, scope, params);
        this.log(record);
    }

    /**
     * Logs a warning message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public warning(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        let record = this.createLogRecord(LogLevel.Warning, msg, scope, params);
        this.log(record);
    }

    /**
     * Logs an error message.
     *
     * @param msg - The text to log.
     * @param scope - The scope of the entry.
     * @param params - Any additional parameters.
     */
    public error(msg: string, scope: string = "", params: LogRecordParameters = {}): void {
        let record = this.createLogRecord(LogLevel.Error, msg, scope, params);
        this.log(record);
    }

    private createLogRecord(level: LogLevel, msg: string, scope: string, params: LogRecordParameters): LogRecord {
        return new LogRecord(msg, new Date(), level, scope, params);
    }

    private log(record: LogRecord): void {
        if (record.level >= this._level) {
            let formatter = new Formatter(record);
            console.log(formatter.formattedText, ...formatter.stylesStack);
        }
    }
}
