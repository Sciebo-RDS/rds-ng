<script setup lang="ts">
import { ref, watch } from "vue";

import Button from "primevue/button";
import Listbox from "primevue/listbox";
import Menu from 'primevue/menu';

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

const menu = ref();
const items = ref([
    {
        label: 'Options',
        items: [
            {
                label: 'Update',
                icon: 'pi pi-refresh',
                command: () => {
                    toast.add({ severity: 'success', summary: 'Updated', detail: 'Data Updated', life: 3000 });
                }
            },
            {
                label: 'Delete',
                icon: 'pi pi-times',
                command: () => {
                    toast.add({ severity: 'warn', summary: 'Delete', detail: 'Data Deleted', life: 3000 });
                }
            }
        ]
    }
]);

const toggle = (event) => {
    menu.value.toggle(event);
};
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
                        <Button text rounded size="small" aria-label="Options" title="More options" class="invisible group-hover:visible" @click="toggle">
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
        <Menu ref="menu" id="overlay_menu" :model="items" :popup="true"/>
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

#project-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>
