import { ProjectObject } from "../ProjectObjectStore";

export function injectTemplate(str: String, obj: ProjectObject) {
    const label = str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? obj["value"][g] : `\${${g}\}`));
    return label === str ? `[${obj["id"].slice(0, 6)}]` : str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? obj["value"][g] : `[${g}]`));
}
