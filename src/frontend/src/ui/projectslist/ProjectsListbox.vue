<script setup lang="ts">
import { storeToRefs } from "pinia";
import { watch } from "vue";
import Listbox from "primevue/listbox";

import { Project, ProjectStatus } from "@common/data/entities/Project";

import { projectsStore } from "@/data/stores/ProjectsStore";
import ProjectsListboxItem from "@/ui/projectslist/ProjectsListboxItem.vue";

const projStore = projectsStore();
const { projects, activeProject } = storeToRefs(projStore);

watch(activeProject, (newProj, oldProj) => {
    // Prevent deselecting the currently selected project item
    if (newProj === null && oldProj) {
        // @ts-ignore
        activeProject.value = oldProj;
    }
});

function isProjectSelected(project: Project): boolean {
    // @ts-ignore
    return project.project_id === activeProject.value;
}

function isProjectDeleted(project: Project): boolean {
    // @ts-ignore
    return project.status == ProjectStatus.Deleted || projStore.pendingDeletions.includes(project.project_id);
}

function onProjectDeleted(project: Project): void {
    if (isProjectSelected(project)) {
        // @ts-ignore
        activeProject.value = undefined;
    }
}
</script>

<template>
    <div>
        <!-- TODO: Add select-on-focus -->
        <Listbox
            v-model="activeProject"
            :options="projects"
            option-value="project_id"
            :option-disabled="isProjectDeleted"
            class="w-full"
            :pt="{
                root: 'projects-listbox',
                list: 'projects-listbox-list',
                item: 'projects-listbox-item',
            }"
        >
            <template #option="projectEntry">
                <ProjectsListboxItem
                    :project="projectEntry.option"
                    :is-selected="isProjectSelected(projectEntry.option)"
                    :is-deleted="isProjectDeleted(projectEntry.option)"
                    @project-deleted="onProjectDeleted"
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
    @apply pr-2 border-solid border-b-2 border-[--r-border-color] #{!important};
}
</style>
