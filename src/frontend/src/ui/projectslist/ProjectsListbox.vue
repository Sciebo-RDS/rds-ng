<script setup lang="ts">
import Button from "primevue/button";
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
        <Listbox v-model="selectedProject" :options="feStore.projects" class="w-full" :pt="{
                root: 'projects-listbox',
                list: 'projects-listbox-list',
                item: 'projects-listbox-item',
            }"
        >
            <template #option="projectEntry">
                <div class="grid grid-rows-[auto_auto] grid-cols-[1fr_min-content] gap-0 h-24 place-content-start group">
                    <div class="r-text-caption-big h-8 truncate" :title="projectEntry.option.name">{{ projectEntry.option.name }}</div>
                    <div class="row-span-2 pl-1">
                        <Button text rounded size="small" aria-label="Options" title="More options" class="invisible group-hover:visible">
                            <template #icon>
                                <span class="material-icons-outlined" :class="[projectEntry.option.project_id === selectedProject?.project_id ? 'r-primary-text' : 'r-text']" style="font-size: 32px;">more_vert</span>
                            </template>
                        </Button>
                    </div>

                    <div id="project-description" class="overflow-hidden line-clamp" :title="projectEntry.option.description">{{ projectEntry.option.description }}</div>
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
    padding-right: 0.5em !important;
    border-bottom: 2px solid var(--r-border-color) !important;
}

#project-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>
