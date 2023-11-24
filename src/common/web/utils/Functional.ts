/**
 * Calls an optional function, i.e. a function that can be undefined.
 *
 * @param cb - The function to call.
 * @param args - Arguments passed to the function.
 */
export function optCall(cb: Function | undefined, ...args: any[]): any | undefined {
    if (cb) {
        return cb(...args);
    }
    return undefined;
}
