import { defineStore } from "pinia";
import { ref } from "vue";

import { Project, type ProjectID } from "@common/data/entities/Project";

/**
 * The projects store for all project-specific data.
 *
 * @param projects - List of all projects.
 */
export const projectsStore = defineStore("projectsStore", () => {
    const projects = ref<Project[]>([]);
    const activeProject = ref<ProjectID | null | undefined>(undefined);

    let pendingDeletions = ref<ProjectID[]>([]);

    function resolveActiveProject(): Project | undefined {
        if (activeProject) {
            const project = projects.value.find(proj => proj.project_id === activeProject.value);
            if (project) {
                return project;
            }
        }
        return undefined;
    }

    function markForDeletion(projectID: ProjectID): void {
        if (!pendingDeletions.value.includes(projectID)) {
            pendingDeletions.value = [...pendingDeletions.value, projectID];

            if (activeProject.value === projectID) {
                activeProject.value = undefined;
            }
        }
    }

    function unmarkForDeletion(projectID: ProjectID): void {
        pendingDeletions.value = pendingDeletions.value.filter(elem => elem != projectID);
    }

    function reset(): void {
        projects.value = [] as Project[];
        activeProject.value = undefined;

        pendingDeletions.value = [] as ProjectID[];
    }

    function resetPendingDeletions(): void {
        pendingDeletions.value = [] as ProjectID[];
    }

    return {
        projects,
        activeProject,
        pendingDeletions,
        resolveActiveProject,
        markForDeletion,
        unmarkForDeletion,
        reset,
        resetPendingDeletions
    };
});
