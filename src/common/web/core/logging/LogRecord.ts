export enum LogLevel {
    Debug = 10,
    Info = 20,
    Warning = 30,
    Error = 40
}

export interface LogRecordParameters {
    [Key: string]: any;
}

export class LogRecord {
    public constructor(readonly msg: string, readonly timestamp: Date, readonly level: LogLevel, readonly scope: string,
                       readonly params: LogRecordParameters) {
    }

    public get levelName(): string {
        try {
            return LogLevel[this.level].toUpperCase();
        } catch {
            return "<unknown>";
        }
    }
}
