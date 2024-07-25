import { SharedObject } from "../ProjectObjectStore";
import { PropertyProfileStore } from "../PropertyProfileStore";
import { calculateClassColor } from "./Colors";
import { injectTemplate } from "./Templates";

/**
 * Calculate a background color for an object
 *
 * @param obj - The linked object.
 * @param profileStore - The PropertyProfileStore that defines the object's class.
 *
 * @returns - A css lch color definition.
 */
export function calcBgColor(obj: SharedObject, profileStore: PropertyProfileStore): string {
    if (obj === undefined) return "#eeeeee";
    return calculateClassColor(obj.type!, 99, 10)["bgColor"];
}

/**
 * Calculate a border color for an object
 *
 * @param obj - The linked object.
 * @param profileStore - The PropertyProfileStore that defines the object's class.
 *
 * @returns - A css lch color definition.
 */
export function calcBorderColor(obj: SharedObject, profileStore: PropertyProfileStore): string {
    if (obj === undefined) return "#ee0000";
    return calculateClassColor(obj.type!, 99, 10)["borderColor"];
}

/**
 * Calculate the display label for an object
 *
 * @param obj - The linked object.
 * @param profileStore - The PropertyProfileStore that defines the object's class.
 *
 * @returns - An object label string.
 */
export function calcObjLabel(obj: SharedObject, profileStore: PropertyProfileStore): string {
    if (obj === undefined) return "";
    const labelTemplate = profileStore.getLabelTemplateById(obj.type!)!;
    return injectTemplate(labelTemplate, obj);
}
