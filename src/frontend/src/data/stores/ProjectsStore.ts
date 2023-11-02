import { defineStore } from "pinia";
import { ref } from "vue";

import { Project, type ProjectID } from "@common/data/entities/Project";

/**
 * The projects store for all project-specific data.
 *
 * @param projects - List of all projects.
 */
export const projectsStore = defineStore("projectStore", () => {
    let projects = ref<Project[]>([]);

    let pendingDeletions = ref<ProjectID[]>([]);

    function markForDeletion(projectID: ProjectID): void {
        if (!pendingDeletions.value.includes(projectID)) {
            pendingDeletions.value = [...pendingDeletions.value, projectID];
        }
    }

    function unmarkForDeletion(projectID: ProjectID): void {
        pendingDeletions.value = pendingDeletions.value.filter(elem => elem != projectID);
    }

    function reset() {
        projects.value = [] as Project[];

        pendingDeletions.value = [] as ProjectID[];
    }

    return {
        projects,
        pendingDeletions,
        markForDeletion,
        unmarkForDeletion,
        reset
    };
});
