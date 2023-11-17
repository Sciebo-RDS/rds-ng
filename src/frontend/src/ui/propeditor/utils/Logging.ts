export class Logger {
    public static info(message: string, source: string) {
        console.log(
            `${new Date().toLocaleString(
                navigator.language
            )} [INFO|${source}] ${message}`
        );
    }

    public static error(message: string, source: string) {
        console.error(
            `${new Date().toLocaleString(
                navigator.language
            )} [ERROR]|${source}] ${message}`
        );
    }

    public static debug(message: string, source: string) {
        console.log(
            `${new Date().toLocaleString(
                navigator.language
            )} [DEBUG|${source}] ${message}`
        );
    }

    public static warning(message: string, source: string) {
        console.warn(
            `${new Date().toLocaleString(
                navigator.language
            )} [WARNING|${source}] ${message}`
        );
    }
}
