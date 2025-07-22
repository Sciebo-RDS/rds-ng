import { ResourcesListCache } from "@/data/entities/resource/ResourcesListCache.ts";
import { defineStore } from "pinia";
import { ref } from "vue";

import { ResourcesDataCache } from "@/data/entities/resource/ResourcesDataCache";

/**
 * Resources store for all resources-related data.
 */
export const useResourcesStore = defineStore("resourcesStore", () => {
    const resourcesListCache = ref(new ResourcesListCache());
    const resourcesDataCache = ref(new ResourcesDataCache());

    return {
        resourcesListCache,
        resourcesDataCache
    };
});
