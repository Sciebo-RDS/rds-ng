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
