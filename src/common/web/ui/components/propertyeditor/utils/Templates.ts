import { formatLocaleTimestamp } from "../../../../utils/Strings";
import { PropertyObject } from "../PropertyObjectStore";

/**
 * Replaces placeholders in a string with corresponding values from a given object.
 * If a placeholder does not have a corresponding value in the object, it is replaced with the placeholder itself.
 * @param str - The string containing placeholders to be replaced.
 * @param obj - The object containing values to replace the placeholders.
 *
 * @returns The string with replaced placeholders.
 */
export function injectTemplate(str: String, obj: PropertyObject) {
    const formatValue = (value: string): string => {
        try {
            // @ts-ignore
            switch (obj.type!) {
                case "date":
                    console.log(value);
                    const dt = Date.parse(value);
                    if (!isNaN(dt)) {
                        return formatLocaleTimestamp(dt / 1000, false);
                    }
            }
        } catch (e) {}

        return value;
    };

    const label = str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? formatValue(obj["value"][g]) : `\${${g}\}`));
    return label === str ? `[${obj["id"].slice(0, 6)}]` : str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? formatValue(obj["value"][g]) : `[${g}]`));
}
