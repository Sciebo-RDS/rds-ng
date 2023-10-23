import { defineStore } from "pinia";
import { reactive } from "vue";

import { Project } from "@common/data/entities/Project";

/**
 * The frontend store for all frontend-specific data.
 *
 * @param projects - List of all projects.
 */
export const frontendStore = defineStore("frontendStore", () => {
    let projects = reactive<Project[]>([]);

    function reset() {
        projects = [] as Project[];
    }

    return {
        projects,
        reset
    };
});
