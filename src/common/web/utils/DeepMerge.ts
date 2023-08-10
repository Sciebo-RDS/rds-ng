function isObject(item: any) {
    return item && typeof item === 'object' && !Array.isArray(item);
}

type MergeObjectType = Record<string | number | symbol, any>;

/**
 * Deep merge two objects.
 *
 * @param target - The target object.
 * @param sources - The source objects to merge into the target.
 */
export function deepMerge(target: MergeObjectType, ...sources: MergeObjectType[]): object {
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

    return deepMerge(target, ...sources);
}
