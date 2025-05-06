export abstract class Logger {
    public static info(message: string, source: string): void {
        console.log(
            `${new Date().toLocaleString(
                navigator.language
            )} [INFO|${source}] ${message}`
        );
    }

    public static error(message: string, source: string): void {
        console.error(
            `${new Date().toLocaleString(
                navigator.language
            )} [ERROR]|${source}] ${message}`
        );
    }

    public static debug(message: string, source: string): void {
        console.log(
            `${new Date().toLocaleString(
                navigator.language
            )} [DEBUG|${source}] ${message}`
        );
    }

    public static warning(message: string, source: string): void {
        console.warn(
            `${new Date().toLocaleString(
                navigator.language
            )} [WARNING|${source}] ${message}`
        );
    }
}
