<script setup lang="ts">
import { ref } from "vue";

import Menu from "primevue/menu";
import Button from "primevue/button";

const props = defineProps(['project', 'isSelected']);
const project = props.project;
const isSelected = props.isSelected;

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
    <div class="grid grid-rows-[auto_auto] grid-cols-[1fr_min-content] gap-0 h-24 place-content-start group">
        <div class="r-text-caption-big h-8 truncate" :title="project.name">{{ project.name }}</div>
        <div class="row-span-2 pl-1">
            <Button text rounded size="small" aria-label="Options" title="More options" class="invisible group-hover:visible" @click="toggle">
                <template #icon>
                    <span class="material-icons-outlined" :class="[isSelected ? 'r-primary-text' : 'r-text']" style="font-size: 32px;">more_vert</span>
                </template>
            </Button>
            <Menu ref="menu" id="overlay_menu" :model="items" :popup="true"/>
        </div>

        <div id="project-description" class="overflow-hidden line-clamp" :title="project.description">{{ project.description }}</div>
    </div>
</template>

<style scoped lang="scss">
#project-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>
