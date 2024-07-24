<script setup lang="ts">
import { computed } from "vue";

import { useProjectsStore } from "@/data/stores/ProjectsStore";

import Contents from "@/ui/content/main/projectdetails/Contents.vue";
import ContentsEmpty from "@/ui/content/main/projectdetails/ContentsEmpty.vue";
import Header from "@/ui/content/main/projectdetails/Header.vue";
import HeaderEmpty from "@/ui/content/main/projectdetails/HeaderEmpty.vue";

const projStore = useProjectsStore();
const currentProject = computed(() => projStore.resolveActiveProject());
</script>

<template>
    <div class="grid grid-rows-[5rem_1fr] grid-cols-1 gap-0 w-full h-full">
        <Header v-if="currentProject" :project="currentProject" />
        <HeaderEmpty v-else />

        <Contents v-if="currentProject" :project="currentProject" />
        <ContentsEmpty v-else />
    </div>
</template>

<style scoped lang="scss"></style>
