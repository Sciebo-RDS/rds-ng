import { GetResourceReply } from "@common/api/resource/ResourceCommands";
import { Resource } from "@common/data/entities/resource/Resource";
import { encodeBase64 } from "@common/utils/Strings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourcesStore } from "@/data/stores/ResourcesStore";
import { GetResourceAction } from "@/ui/actions/resource/GetResourceAction";

export function useResourceTools(comp: FrontendComponent) {
    async function retrieveResourceData(resource: Resource): Promise<ArrayBuffer | undefined> {
        const resourcesStore = useResourcesStore();

        return new Promise<ArrayBuffer | undefined>((resolve, reject) => {
            if (resourcesStore.resourcesCache.hasData(resource)) {
                resourcesStore.resourcesCache.bump(resource);
                resolve(resourcesStore.resourcesCache.getData(resource));
            } else {
                const action = new GetResourceAction(comp, true);
                action
                    .prepare(resource)
                    .done((reply: GetResourceReply) => {
                        if (!!reply.data) {
                            resourcesStore.resourcesCache.push(resource, reply.data);
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
        retrieveResourceData,
        resourceDataToTagValue,
        resourceDataToBlob
    };
}
