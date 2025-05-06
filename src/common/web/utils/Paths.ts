/**
 * Extracts the filename (i.e., last element) of a complete path.
 *
 * @param path - The full path.
 *
 * @returns - The filename/last element of the path.
 */
export function extractFilenameFromPath(path: string): string {
    return path.replace("\\", "/").split("/").pop() || "";
}

/**
 * Terminates a path with a slash.
 *
 * @param path - The original path.
 *
 * @returns - The terminated path.
 */
export function terminatePath(path: string): string {
    return !path.endsWith("/") ? path + "/" : path;
}
