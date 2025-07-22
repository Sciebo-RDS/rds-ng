import { GetResourceReply, ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Resource } from "@common/data/entities/resource/Resource";
import { ResourcesList } from "@common/data/entities/resource/ResourcesList.ts";
import { encodeBase64 } from "@common/utils/Strings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourcesStore } from "@/data/stores/ResourcesStore";
import { GetResourceAction } from "@/ui/actions/resource/GetResourceAction";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction.ts";

export function useResourceTools(comp: FrontendComponent) {
    async function retrieveResourcesList(path: string, recursive: boolean = true): Promise<ResourcesList> {
        const resourcesStore = useResourcesStore();

        return new Promise<ResourcesList>(async (resolve, reject) => {
            const resources = resourcesStore.resourcesListCache.getPath(path);
            if (!!resources) {
                resolve(resources);
            } else {
                const action = new ListResourcesAction(comp, true);
                action
                    .prepare(path, true, true, recursive)
                    .done((reply: ListResourcesReply, success, msg) => {
                        if (success) {
                            resourcesStore.resourcesListCache.push(reply.resources);
                            resolve(reply.resources);
                        } else {
                            reject(`Unable to fetch ${path}: ${msg}`);
                        }
                    })
                    .failed((_, reason) => {
                        reject(`Unable to fetch ${path}: ${reason}`);
                    });
                action.execute();
            }
        });
    }

    function clearResourcesListCache(): void {
        const resourcesStore = useResourcesStore();

        resourcesStore.resourcesListCache.clear();
    }

    async function retrieveResourceData(resource: Resource): Promise<ArrayBuffer | undefined> {
        const resourcesStore = useResourcesStore();

        return new Promise<ArrayBuffer | undefined>((resolve, reject) => {
            if (resourcesStore.resourcesDataCache.hasData(resource)) {
                resourcesStore.resourcesDataCache.bump(resource);
                resolve(resourcesStore.resourcesDataCache.getData(resource));
            } else {
                const action = new GetResourceAction(comp, true);
                action
                    .prepare(resource)
                    .done((reply: GetResourceReply) => {
                        if (!!reply.data) {
                            resourcesStore.resourcesDataCache.push(resource, reply.data);
                        }
                        resolve(reply.data);
                    })
                    .failed((_, reason: string) => {
                        reject(reason);
                    });
                action.execute();
            }
        });
    }

    function resourceDataToTagValue(resource: Resource, data: ArrayBuffer | undefined): string {
        return !!data ? `data:${resource.mime_type};base64,${encodeBase64(data)}` : "";
    }

    function resourceDataToBlob(resource: Resource, data: ArrayBuffer | undefined): string {
        if (!!data) {
            return URL.createObjectURL(new Blob([data], { type: resource.mime_type }));
        }
        return "";
    }

    return {
        retrieveResourcesList,
        clearResourcesListCache,
        retrieveResourceData,
        resourceDataToTagValue,
        resourceDataToBlob
    };
}
