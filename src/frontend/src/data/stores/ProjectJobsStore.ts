import { defineStore } from "pinia";
import { ref } from "vue";

import { ProjectJob } from "@common/data/entities/project/ProjectJob";

/**
 * The project jobs store for all project job-specific data.
 *
 * @param jobs - List of all project jobs.
 */
export const useProjectJobsStore = defineStore("projectJobsStore", () => {
    const jobs = ref<ProjectJob[]>([]);

    function reset(): void {
        jobs.value = [] as ProjectJob[];
    }

    return {
        jobs,
        reset,
    };
});
