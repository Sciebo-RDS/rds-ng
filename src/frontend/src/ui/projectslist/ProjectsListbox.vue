<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";
import Listbox from "primevue/listbox";

import { Project, ProjectStatus } from "@common/data/entities/Project";

import { projectsStore } from "@/data/stores/ProjectsStore";
import ProjectsListboxItem from "@/ui/projectslist/ProjectsListboxItem.vue";

const projStore = projectsStore();
const { projects } = storeToRefs(projStore);

const selectedProject = ref<Project | null | undefined>(undefined);
watch(selectedProject, (newProj, oldProj) => {
    // Prevent deselecting the currently selected project item
    if (newProj === null && oldProj) {
        selectedProject.value = oldProj;
    }
});

function isProjectSelected(project: Project): boolean {
    return project.project_id === selectedProject?.value?.project_id;
}

function isProjectDeleted(project: Project): boolean {
    return (project.status == ProjectStatus.Deleted) || (projStore.pendingDeletions.includes(project.project_id));
}

function onProjectDeleted(project: Project): void {
    if (isProjectSelected(project)) {
        selectedProject.value = undefined;
    }
}
</script>

<template>
    <div>
        <Listbox v-model="selectedProject" :options="projects" :option-disabled="isProjectDeleted" class="w-full" :pt="{
                root: 'projects-listbox',
                list: 'projects-listbox-list',
                item: 'projects-listbox-item',
            }"
        >
            <template #option="projectEntry">
                <ProjectsListboxItem :project="projectEntry.option" :is-selected="isProjectSelected(projectEntry.option)" :is-deleted="isProjectDeleted(projectEntry.option)" @project-deleted="onProjectDeleted"/>
            </template>
            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No current projects</div>
            </template>
        </Listbox>
    </div>
</template>

<style scoped lang="scss">
:deep(.projects-listbox) {
    @apply border-0 rounded-none bg-inherit #{!important};
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
