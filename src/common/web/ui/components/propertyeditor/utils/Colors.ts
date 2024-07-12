import { type ProfileID } from "../PropertyProfile";
import { PropertyProfileStore } from "../PropertyProfileStore";

/**
 * Calculates the color for a property class based on the given parameters.
 * @param projectProfiles - The property profile store.
 * @param profileId - The profile ID.
 * @param type - The class type.
 * @param brightness - The brightness value.
 * @param chroma - The chroma value.
 *
 * @returns An object containing css-lch definitions for background color and border color.
 */
export function calculateClassColor(projectProfiles: PropertyProfileStore, profileId: ProfileID, type: string, brightness: number, chroma: number) {
    const objectClass = projectProfiles.getClassById(profileId, type);
    const classes = projectProfiles.listClasses();
    const position = classes.findIndex((e) => e.id == objectClass?.id);
    const hue = (360 / projectProfiles.listClasses().length) * position;

    return {
        bgColor: `lch(${brightness}% ${chroma} ${hue})`,
        borderColor: `lch(${(brightness - 19) % 100}% ${(chroma + 10) % 100} ${hue})`
    };
}

/**
 * Converts a string to a color value.
 * @param str - The string to convert.
 * @param alpha - The alpha value of the color (optional, default is 1).
 *
 * @returns The css-lch definition of the color value.
 */
export function stringToColor(str: any, alpha: number = 1) {
    var num = 0;
    for (let i in str) num += str.charCodeAt(i);
    return `lch(90 25 ${num % 360} / ${alpha})`;
}
