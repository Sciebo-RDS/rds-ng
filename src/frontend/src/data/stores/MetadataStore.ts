import { defineStore } from "pinia";
import { ref } from "vue";

import { type MetadataProfileContainerList } from "@common/data/entities/metadata/MetadataProfileContainer";

/**
 * The metadata store for all metadata-specific data.
 *
 * @param connectors - List of all connectors.
 */
export const useMetadataStore = defineStore("metadataStore", () => {
    const profiles = ref<MetadataProfileContainerList>([]);

    function reset(): void {
        profiles.value = [] as MetadataProfileContainerList;
    }

    return {
        profiles,
        reset
    };
});
