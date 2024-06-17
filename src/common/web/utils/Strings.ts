/**
 * Converts an arbitrary value or an array of such to a string array.
 *
 * @param value - The value to convert.
 * @param delimiter - The delimiter to use for splitting a non-array value.
 */
export function convertToStringArray(value: any | any[], delimiter: string = " "): string[] {
    if (value === null || value === undefined) {
        return [];
    } else if (Array.isArray(value)) {
        let arr: string[] = [];
        value.forEach((obj) => {
            arr.push(String(obj));
        });
        return arr;
    } else {
        return String(value).split(delimiter);
    }
}

/**
 * Converts a file size (in bytes) to a human-readable form.
 *
 * @param size - The file size in bytes.
 *
 * @returns - A string representation of the size.
 */
export function humanReadableFileSize(size: number): string {
    try {
        const i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
        return (size / Math.pow(1024, i)).toFixed(1) + " " + ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"][i];
    } catch {
        return size + " B";
    }
}

/**
 * Formats a UNIX timestamp to a string using the system locale.
 *
 * @param date - The timestamp.
 *
 * @returns - The formatted string.
 */
export function formatLocaleTimestamp(date: number): string {
    return new Intl.DateTimeFormat(navigator.language, { dateStyle: "medium", timeStyle: "short" }).format(date * 1000);
}

/**
 * Adds a full stop to a string if necessary.
 *
 * @param sentence - The sentence to complete.
 */
export function finishSentence(sentence: string): string {
    if (sentence.length > 0 && sentence[sentence.length - 1] != ".") {
        sentence += ".";
    }
    return sentence;
}

/**
 * Formats a number of seconds into a readable form.
 *
 * @param elapsed - The elapsed time in seconds.
 *
 * @returns - The formatted string.
 */
export function formatElapsedTime(elapsed: number): string {
    const days = Math.floor(elapsed / (60 * 60 * 24));
    elapsed -= days * (60 * 60 * 24);

    const hours = Math.floor(elapsed / (60 * 60));
    elapsed -= hours * (60 * 60);

    const mins = Math.floor(elapsed / 60);
    elapsed -= mins * 60;

    const seconds = Math.floor(elapsed);
    elapsed -= seconds;

    const tokens: String[] = [];

    function adcToken(val: number, name: string) {
        if (val >= 1.0) {
            tokens.push(`${val}${name}`);
        }
    }

    adcToken(days, "d");
    adcToken(hours, "h");
    adcToken(mins, "m");
    adcToken(seconds, "s");

    return tokens.join(" ");
}
