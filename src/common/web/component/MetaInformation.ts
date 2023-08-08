import { SemVer } from "semver";

import metaData from "/config/meta-information.json";

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
    private readonly _title: string;
    private readonly _version: SemVer;
    private readonly _components: object;

    public constructor() {
        [this._title, this._version] = this.readGlobalInfo(metaData);
        this._components = this.readComponentDefinitions(metaData);
    }

    private readGlobalInfo(data: object): [string, SemVer] {
        try {
            let globalInfo = data["global"];
            let title = globalInfo["title"];
            let version = globalInfo["version"];
            return [title, new SemVer(version)];
        } catch {
            return ["<invalid>", new SemVer("0.0.0")]
        }
    }

    private readComponentDefinitions(data: object) {
        try {
            return data["components"];
        } catch {
            return {};
        }
    }

    /**
     * The project title.
     */
    public get title() {
        return this._title;
    }

    /**
     * The project version (see https://semver.org).
     */
    public get version() {
        return this._version;
    }

    /**
     * A list of all component names.
     *
     * @returns - The names of all components.
     */
    public getComponents() {
        return Object.keys(this._components);
    }

    /**
     * Retrieves the meta information stored for a specific component.
     *
     * This meta information includes the ``name`` of the component, as well as its ``directory`` within the code structure (rooted at ``/src``).
     *
     * @param comp - The name of the component.
     *
     * @returns - A dictionary containing the meta information.
     */
    public getComponent(comp: string) {
        if (comp in this._components) {
            return this._components[comp];
        }

        return {
            "name": "<invalid>",
            "directory": "",
            "tech": "",
        };
    }
}
