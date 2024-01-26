<script setup lang="ts">
// @ts-nocheck

import { useProjectTools } from "@/ui/tools/ProjectTools";
import { storeToRefs } from "pinia";
import Listbox from "primevue/listbox";
import { watch } from "vue";
import { useRoute } from "vue-router";

import { Project, type ProjectID, ProjectStatus } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useProjectsStore } from "@/data/stores/ProjectsStore";

import ProjectsListboxItem from "@/ui/content/main/projectslist/ProjectsListboxItem.vue";

const comp = FrontendComponent.inject();
const route = useRoute();
const projStore = useProjectsStore();
const { projects, activeProject } = storeToRefs(projStore);
const { editProject, deleteProject } = useProjectTools(comp);

const unwatchProjects = watch(projects, () => {
    // If the current URL contains a project ID, select that project once we received our projects list
    if (route.params.hasOwnProperty("project_id")) {
        let projectID = route.params.project_id as string;
        selectProject(parseInt(projectID), true);
    }

    unwatchProjects();
});

watch(activeProject, (newProj, oldProj) => {
    // Prevent deselecting the currently selected project item
    if (newProj === null && oldProj) {
        activeProject.value = oldProj;
    }

    // Update the shown URL to reflect the selected project
    if (activeProject.value !== oldProj) {
        comp.userInterface.frontendView.navigateTo(true, undefined, { project_id: activeProject.value });
    }
});

function selectProject(projectID: ProjectID | undefined, autoNavigateOnMissing: boolean = false): void {
    if (!projects.value.find((proj) => proj.project_id === projectID)) {
        projectID = undefined;

        if (autoNavigateOnMissing) {
            comp.userInterface.frontendView.navigateTo(true);
        }
    }
    activeProject.value = projectID;
}

function isProjectSelected(project: Project): boolean {
    return project.project_id === activeProject.value;
}

function isProjectDeleted(project: Project): boolean {
    return project.status == ProjectStatus.Deleted || projStore.pendingDeletions.includes(project.project_id);
}
</script>

<template>
    <div>
        <Listbox
            v-model="activeProject"
            :options="projects"
            option-value="project_id"
            :option-disabled="isProjectDeleted"
            class="w-full"
            :pt="{
                root: 'projects-listbox',
                list: 'projects-listbox-list',
                item: 'projects-listbox-item'
            }"
        >
            <template #option="projectEntry">
                <ProjectsListboxItem
                    :project="projectEntry.option"
                    :is-selected="isProjectSelected(projectEntry.option)"
                    :is-deleted="isProjectDeleted(projectEntry.option)"
                    @dblclick="editProject(projectEntry.option)"
                    @edit-project="editProject(projectEntry.option)"
                    @delete-project="deleteProject(projectEntry.option)"
                />
            </template>
            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No current projects</div>
            </template>
        </Listbox>
    </div>
</template>

<style scoped lang="scss">
:deep(.projects-listbox) {
    // Max height is 100% - header height (5rem) - footer height (6rem)
    @apply border-0 rounded-none bg-inherit overflow-y-auto max-h-[calc(100vh-5rem-6rem)] #{!important};
}

:deep(.projects-listbox.p-focus) {
    @apply shadow-none #{!important};
}

:deep(.projects-listbox-list) {
    @apply p-0 #{!important};
}

:deep(.projects-listbox-item) {
    @apply pr-2 border-solid border-b border-[--r-border-color] #{!important};
}
</style>
