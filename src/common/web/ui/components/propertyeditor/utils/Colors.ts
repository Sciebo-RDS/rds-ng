import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { type ProfileID } from "../PropertyProfile";


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
export function calculateClassColor(type: string, brightness: number, chroma: number) {
    return {
        bgColor: `lch(${brightness}% ${chroma} ${_stringToHue(type)})`,
        borderColor: `lch(${(brightness - 19) % 100}% ${(chroma + 10) % 100} ${_stringToHue(type)})`
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
    return `lch(90 25 ${_stringToHue(str)} / ${alpha})`;
}

function _stringToHue(str: any) {
    const chars = [...str];
    var num = 0;
    chars.forEach((char, i) => {
        num += str.charCodeAt(i) * i + 57;
    });
    return num % 360;
}

export function profileToColor(profileID: ProfileID) {
    const conStore = useConnectorsStore();

    const profileIndex = [["DataCite", ""], ...conStore.connectors.map((e) => e.metadata_profile.metadata.id)]
        .sort()
        .findIndex((c) => c[0] == profileID[0]);

    const hue = profileIndex * (360 / conStore.connectors.length);

    return `lch(90 25 ${hue})`;
}