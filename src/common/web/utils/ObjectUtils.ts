import { humanReadableFileSize } from "./Strings";

function isObject(item: any) {
    return item && typeof item === "object" && !Array.isArray(item);
}

type CloneObjectType = Record<string | number | symbol, any>;

/**
 * Deep-merge two objects.
 *
 * @param target - The target object.
 * @param sources - The source objects to merge into the target.
 */
export function deepMerge<ObjType = object>(target: CloneObjectType, ...sources: CloneObjectType[]): ObjType {
    if (!sources.length) {
        return target;
    }

    const source = sources.shift();
    if (isObject(target) && isObject(source)) {
        for (const key in source) {
            if (isObject(source[key])) {
                if (!target[key]) {
                    Object.assign(target, { [key]: {} });
                }
                deepMerge(target[key], source[key]);
            } else {
                Object.assign(target, { [key]: source[key] });
            }
        }
    }

    return deepMerge<ObjType>(target, ...sources);
}

/**
 * Deep-clones an object.
 *
 * @param source - The source object; if this is undefined, the default value is used.
 * @param defaultValue - The default value if the source is undefined.
 */
export function deepClone<ObjType = object>(source?: CloneObjectType, defaultValue?: CloneObjectType): ObjType {
    if (!source && !defaultValue) {
        throw new Error("Tried to deep-clone an object without a source and default value");
    }

    if (!source) {
        return defaultValue!;
    }
    return JSON.parse(JSON.stringify(source)) as ObjType;
}

/**
 * Shortens data strings in an object for better display.
 *
 * @param obj - The object to clean up.
 */
export function shortenDataStrings(obj: any): any {
    for (const [name, value] of Object.entries(obj)) {
        if (typeof value === "object") {
            shortenDataStrings(value);
        } else if (typeof value === "string") {
            if (value.startsWith("data:")) {
                obj[name] = value.split(",", 1).join() + `,<data:${humanReadableFileSize(value.length)}>`;
            }
        }
    }

    return obj;
}
