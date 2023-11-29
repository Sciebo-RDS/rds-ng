<script setup lang="ts">
import { computed } from "vue";

import { projectsStore } from "@/data/stores/ProjectsStore";

import Contents from "@/ui/content/projectdetails/Contents.vue";
import ContentsEmpty from "@/ui/content/projectdetails/ContentsEmpty.vue";
import Header from "@/ui/content/projectdetails/Header.vue";
import HeaderEmpty from "@/ui/content/projectdetails/HeaderEmpty.vue";

const projStore = projectsStore();
const currentProject = computed(() => projStore.resolveActiveProject());
</script>

<template>
    <div class="grid grid-rows-[5rem_1fr] grid-cols-1 gap-0 w-full">
        <Header v-if="currentProject" :project="currentProject" />
        <HeaderEmpty v-else />

        <Contents v-if="currentProject" :project="currentProject" />
        <ContentsEmpty v-else />
    </div>
</template>

<style scoped lang="scss">
</style>
