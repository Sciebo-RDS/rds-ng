import { LogRecord } from "./LogRecord";

export class Formatter {
    private static _colors = {
        "default": "#000000",
        "time": "#808080",
        "scope": "#008700",
        "levels": {
            "DEBUG": "#626262",
            "INFO": "#005FFF",
            "WARNING": "#FFAF00",
            "ERROR": "#D70000"
        },
        "params": {
            "name": "#8700FF",
            "value": "#AF0087"
        }
    };

    private _formattedText: string = "";
    private _stylesStack: string[] = [];

    public constructor(record: LogRecord) {
        this.format(record);
    }

    private format(record: LogRecord): void {
        let tokens = [
            this.colorWrap(this.getTimestampString(record), Formatter._colors.time),
            this.colorWrap(" [", Formatter._colors.default),
            this.colorWrapEx(record.levelName, this.getLevelColor(record.levelName), true, false),
            record.scope ? this.colorWrap("|", Formatter._colors.default) + this.colorWrap(record.scope, Formatter._colors.scope) : "",
            this.colorWrap("] ", Formatter._colors.default),
            this.colorWrap(record.msg, Formatter._colors.default),
            Object.entries(record.params).length > 0 ? this.colorWrap(" (", Formatter._colors.default) +
                this.getParametersList(record) + this.colorWrap(")", Formatter._colors.default) : ""
        ];

        this._formattedText = tokens.join("");
    }

    public get formattedText(): string {
        return this._formattedText;
    }

    public get stylesStack(): string[] {
        return this._stylesStack;
    }

    private colorWrap(text: string, color: string): string {
        return this.colorWrapEx(text, color, false, false);
    }

    private colorWrapEx(text: string, color: string, bold: boolean, italic: boolean): string {
        let styles = [`color: ${color};`];
        if (bold) {
            styles.push("font-weight: bold;");
        }
        if (italic) {
            styles.push("font-style: italic;");
        }
        this._stylesStack.push(styles.join(" "));
        return `%c${text}`;
    }

    private getLevelColor(levelName: string): string {
        if (levelName in Formatter._colors.levels) {
            return Formatter._colors.levels[levelName as (keyof typeof Formatter._colors.levels)];
        }
        return Formatter._colors.default;
    }

    private getParametersList(record: LogRecord): string {
        let paramsList: string[] = [];
        let objEntries = Object.entries(record.params);
        for (let i = 0; i < objEntries.length; ++i) {
            let [key, value] = objEntries[i];
            let tokens = [
                this.colorWrapEx(key, Formatter._colors.params.name, false, false),
                this.colorWrap("=", Formatter._colors.default),
                this.colorWrapEx(value, Formatter._colors.params.value, false, true),
            ];
            if (i < objEntries.length - 1) {
                tokens.push(this.colorWrap("; ", Formatter._colors.default));
            }
            paramsList.push(tokens.join(""));
        }
        return paramsList.join("");
    }

    private getTimestampString(record: LogRecord): string {
        let str = record.timestamp.toISOString().replace("T", " ");
        return str.slice(0, str.length - 5);
    }
}
