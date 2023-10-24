<script setup lang="ts">
import { Project } from "@common/data/entities/Project";
import Listbox from "primevue/listbox";
import { ref, watch } from "vue";

import { frontendStore } from "@/data/stores/FrontendStore";

const feStore = frontendStore();

const selectedProject = ref<Project>();

watch(selectedProject, (n, o) => {
        console.log(n)
    }
)
</script>

<template>
    <div>
        <Listbox v-model="selectedProject" :options="feStore.projects" class="w-full" :pt="{ list: { style: 'padding: 0;' }, item: { style: 'border-bottom: 2px solid rgb(209 213 219);' } }">
            <template #option="projectEntry">
                <div class="grid grid-rows-[auto_auto] grid-cols-1 gap-0 text">
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
.p-listbox {
    background-color: inherit;
    border: none;
    border-radius: 0;
}

.p-listbox.p-focus {
    box-shadow: none;
}
</style>
