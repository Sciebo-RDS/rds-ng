import { type ProfileID } from "../PropertyProfile";
import { PropertyProfileStore } from "../PropertyProfileStore";

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

export function stringToColor(str: any, alpha: number = 1) {
    var num = 0;
    for (let i in str) num += str.charCodeAt(i);
    return `lch(90 25 ${num % 360} / ${alpha})`;
}
