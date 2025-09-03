// @ts-ignore
import metaData from "/config/meta-information.json";

import { SemVer } from "semver";

type ComponentInformationType = {
    name: string;
    directory: string;
    tech: string;
};

type MetaInformationType = {
    global: {
        title: string;
        version: string;
    };
};

/**
 * Accesses meta information about the entire project stored in a *JSON* file.
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
}
