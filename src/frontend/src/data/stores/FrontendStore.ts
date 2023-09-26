import { defineStore } from "pinia";
import { ref } from "vue";

import { Project } from "@common/data/entities/Project";

/**
 * The frontend store for all frontend-specific data.
 *
 * @param projects - List of all projects.
 */
export const frontendStore = defineStore("frontendStore", () => {
    const projects = ref<Project[]>([]);

    function reset() {
        projects.value = [] as Project[];
    }

    return {
        projects,
        reset
    };
});
