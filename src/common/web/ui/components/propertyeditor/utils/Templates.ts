import { ProjectObject } from "../ProjectObjectStore";

/**
 * Replaces placeholders in a string with corresponding values from a given object.
 * If a placeholder does not have a corresponding value in the object, it is replaced with the placeholder itself.
 * @param str - The string containing placeholders to be replaced.
 * @param obj - The object containing values to replace the placeholders.
 *
 * @returns The string with replaced placeholders.
 */
export function injectTemplate(str: String, obj: ProjectObject) {
    const label = str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? obj["value"][g] : `\${${g}\}`));
    return label === str ? `[${obj["id"].slice(0, 6)}]` : str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? obj["value"][g] : `[${g}]`));
}
