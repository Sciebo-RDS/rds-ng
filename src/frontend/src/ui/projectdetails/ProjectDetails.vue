<script setup lang="ts">
import { computed } from "vue";

import { projectsStore } from "@/data/stores/ProjectsStore";

import Contents from "@/ui/projectdetails/Contents.vue";
import Header from "@/ui/projectdetails/Header.vue";

const projStore = projectsStore();
const currentProject = computed(() => projStore.resolveActiveProject());
</script>

<template>
    <div class="grid grid-rows-[5rem_1fr] grid-cols-1 gap-0 w-full">
        <Header :project="currentProject" />
        <Contents :project="currentProject" />
    </div>
</template>

<style scoped lang="scss">
</style>
