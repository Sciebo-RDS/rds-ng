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
