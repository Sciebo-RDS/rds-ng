import { defineStore } from "pinia";
import { ref } from "vue";

import { ProjectExporterDescriptor } from "@common/data/exporters/ProjectExporterDescriptor";

/**
 * The exporters store for all project exporters data.
 *
 * @param exporters - List of all exporters.
 */
export const useProjectExportersStore = defineStore("projectExportersStore", () => {
    const exporters = ref<ProjectExporterDescriptor[]>([]);

    function reset(): void {
        exporters.value = [] as ProjectExporterDescriptor[];
    }

    return {
        exporters,
        reset
    };
});
