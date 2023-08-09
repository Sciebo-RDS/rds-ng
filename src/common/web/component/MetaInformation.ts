import { SemVer } from "semver";

import metaData from "/config/meta-information.json"

type ComponentInformationType = {
    name: string;
    directory: string;
    tech: string;
}

type MetaInformationType = {
    global: {
        title: string;
        version: string;
    };
    components: {
        [key: string]: ComponentInformationType;
    };
}

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
    private readonly _data = metaData as MetaInformationType;

    /**
     * The project title.
     */
    public get title(): string {
        return this._data.global.title;
    }

    /**
     * The project version (see https://semver.org).
     */
    public get version(): SemVer {
        return new SemVer(this._data.global.version);
    }

    /**
     * A list of all component names.
     *
     * @returns - The names of all components.
     */
    public getComponents(): string[] {
        return Object.keys(metaData.components);
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
    public getComponent(comp: string): ComponentInformationType {
        if (comp in this._data.components) {
            return this._data.components[comp];
        }

        return {
            "name": "<invalid>",
            "directory": "",
            "tech": "",
        };
    }
}
