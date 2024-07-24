import { GetResourceReply } from "@common/api/resource/ResourceCommands";
import { Resource } from "@common/data/entities/resource/Resource";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourcesStore } from "@/data/stores/ResourcesStore";
import { GetResourceAction } from "@/ui/actions/resource/GetResourceAction";

export function useResourceTools(comp: FrontendComponent) {
    async function retrieveResourceData(resource: Resource): Promise<string> {
        const resourcesStore = useResourcesStore();

        return new Promise<string>((resolve, reject) => {
            if (resourcesStore.resourcesCache.hasData(resource)) {
                resourcesStore.resourcesCache.bump(resource);
                resolve(resourcesStore.resourcesCache.getData(resource));
            } else {
                const action = new GetResourceAction(comp, true);
                action
                    .prepare(resource)
                    .done((reply: GetResourceReply) => {
                        resourcesStore.resourcesCache.push(resource, reply.data);
                        resolve(reply.data);
                    })
                    .failed((_, reason: string) => {
                        reject(reason);
                    });
                action.execute();
            }
        });
    }

    function resourceDataToTagValue(resource: Resource, data: string): string {
        return `data:${resource.mime_type};base64,${data}`;
    }

    return {
        retrieveResourceData,
        resourceDataToTagValue,
    };
}
