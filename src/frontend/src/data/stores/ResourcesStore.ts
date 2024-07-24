import { defineStore } from "pinia";
import { ref } from "vue";

import { ResourcesDataCache } from "@/data/entities/resource/ResourcesDataCache";

/**
 * Resources store for all resources-related data.
 */
export const useResourcesStore = defineStore("resourcesStore", () => {
    const resourcesCache = ref(new ResourcesDataCache());

    return {
        resourcesCache,
    };
});
