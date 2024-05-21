import { PropertyProfileStore } from "../PropertyProfileStore";

export function calculateClassColor(projectProfiles: PropertyProfileStore, profileId: string, type: string, brightness: number, chroma: number) {
    const objectClass = projectProfiles.getClassById(profileId, type);
    const position = projectProfiles.listClasses().findIndex((e) => e.id == objectClass.id);
    const hue = (360 / projectProfiles.listClasses().length) * position;

    return {
        bgColor: `lch(${brightness}% ${chroma} ${hue})`,
        borderColor: `lch(${(brightness - 19) % 100}% ${(chroma + 20) % 100} ${hue})`
    };
}
