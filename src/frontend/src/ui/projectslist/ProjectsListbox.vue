<script setup lang="ts">
import Listbox from "primevue/listbox";
import { ref, watch } from "vue";

import { Project } from "@common/data/entities/Project";

import { frontendStore } from "@/data/stores/FrontendStore";

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
        <Listbox v-model="selectedProject" :options="feStore.projects" lass="w-full" :pt="{
                root: 'projects-listbox',
                list: 'projects-listbox-list',
                item: 'projects-listbox-item',
            }"
        >
            <template #option="projectEntry">
                <div class="grid grid-rows-[auto_auto] grid-cols-1 gap-0">
                    <div class="r-text-caption-big">{{ projectEntry.option.name }}</div>
                    <div>{{ projectEntry.option.description }}</div>
                </div>
            </template>
            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No current projects</div>
            </template>
        </Listbox>
    </div>
</template>

<style scoped lang="scss">
:deep(.projects-listbox) {
    background-color: inherit;
    border: none;
    border-radius: 0;
}

:deep(.projects-listbox.p-focus) {
    box-shadow: none;
}

:deep(.projects-listbox-list) {
    padding: 0 !important;
}

:deep(.projects-listbox-item) {
    border-bottom: 2px solid var(--r-border-color) !important;
}
</style>
