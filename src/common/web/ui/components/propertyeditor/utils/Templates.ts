export function injectTemplate(str: String, obj: Object) {
    const label = str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? obj["value"][g] : `\${${g}\}`));
    return label === str ? `[${obj["id"].slice(-6)}]` : str.replace(/\${(.*?)}/g, (x, g) => (obj["value"][g] ? obj["value"][g] : `[${g}]`));
}
