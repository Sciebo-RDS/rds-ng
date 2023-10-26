<script setup lang="ts">
import { ref, watch } from "vue";

import Listbox from "primevue/listbox";

import { Project } from "@common/data/entities/Project";

import { frontendStore } from "@/data/stores/FrontendStore";
import ProjectsListboxItem from "@/ui/projectslist/ProjectsListboxItem.vue";

const feStore = frontendStore();

const selectedProject = ref<Project | null>(null);
watch(selectedProject, (newProj, oldProj) => {
    // Prevent deselecting the currently selected project item
    if (!newProj && oldProj) {
        selectedProject.value = oldProj;
    }
});
</script>

<template>
    <div>
        <Listbox v-model="selectedProject" :options="feStore.projects" class="w-full" :pt="{
                root: 'projects-listbox',
                list: 'projects-listbox-list',
                item: 'projects-listbox-item',
            }"
        >
            <template #option="projectEntry">
                <ProjectsListboxItem :project="projectEntry.option" :is-selected="projectEntry.option.project_id === selectedProject?.project_id"/>
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
