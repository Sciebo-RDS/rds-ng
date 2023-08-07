/**
 * Accesses meta information about the entire project and its various component stored in a *JSON* file.
 *
 * The JSON file needs to be structured like this:
 * ```
 * {
 *     "global": {
 *         "title": "RDS-NG",
 *         "version": "0.0.1"
 *     },
 *     "components": {
 *         "web-frontend": {
 *             "name": "Web Frontend",
 *             "directory": "frontend",
 *             "tech": "web"
 *         },
 *         ...
 *     }
 * }
 * ```
 */
export class MetaInformation {
    /**
     * @param infoFile - The JSON file to load the meta information from.
     *
     * @throws Error - If the information file couldn't be loaded.
     */
    public constructor(infoFile: string = "/config/meta-information.json") {
    }
}
