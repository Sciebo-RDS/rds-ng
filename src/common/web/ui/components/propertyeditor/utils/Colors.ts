import { PropertyProfileStore } from "../PropertyProfileStore";
import { type ProfileID } from "../PropertyProfile";

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
