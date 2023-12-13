function isObject(item: any) {
    return item && typeof item === "object" && !Array.isArray(item);
}

type MergeObjectType = Record<string | number | symbol, any>;

/**
 * Deep-merge two objects.
 *
 * @param target - The target object.
 * @param sources - The source objects to merge into the target.
 */
export function deepMerge<ObjType = object>(target: MergeObjectType, ...sources: MergeObjectType[]): ObjType {
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
 * Deep-clones an object into another one.
 *
 * @param target - The target object.
 * @param source - The source object, if any.
 */
export function deepClone<ObjType = object>(target: MergeObjectType, source?: MergeObjectType): ObjType {
    return deepMerge<ObjType>(target, source ? source : {});
}
