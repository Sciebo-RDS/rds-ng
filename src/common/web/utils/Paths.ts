/**
 * Extracts the filename (i.e., last element) of a complete path.
 *
 * @param path - The full path.
 *
 * @returns - The filename/last element of the path.
 */
export function extractFilenameFromPath(path: string): string {
    try {
        return path.replace("\\", "/").split("/").pop();
    } catch {
        return "";
    }
}
