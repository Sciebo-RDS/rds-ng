import { ResourcesList } from "./ResourcesList";

/**
 * Statistics about resources.
 */
export interface ResourcesStatistics {
    totalFileCount: number;
    totalFolderCount: number;
    totalSize: number;
}

/**
 * Collects various statistics about resources.
 */
export class ResourcesStatistics {
    private readonly _resources: ResourcesList;

    private readonly _resourcesStatistics: ResourcesStatistics;

    public constructor(resources: ResourcesList) {
        this._resources = resources;
        this._resourcesStatistics = this.createEmptyResourcesStatistics();

        if (!!this._resources) {
            this.collectResourcesStatistics();
        }
    }

    /**
     * Gets statistics about the resources.
     */
    public getResourcesStatistics(): ResourcesStatistics {
        return this._resourcesStatistics;
    }

    private collectResourcesStatistics(): void {
        this.countFilesAndFolders(this._resources);
        this._resourcesStatistics.totalSize = this._resources.resource.size;
    }

    private createEmptyResourcesStatistics(): ResourcesStatistics {
        return {
            totalFileCount: 0,
            totalFolderCount: 1,
            totalSize: 0,
        } as ResourcesStatistics;
    }

    private countFilesAndFolders(resources: ResourcesList): void {
        this._resourcesStatistics.totalFileCount += resources.files.length;
        this._resourcesStatistics.totalFolderCount += resources.folders.length;

        for (const folder of resources.folders) {
            this.countFilesAndFolders(folder);
        }
    }
}
