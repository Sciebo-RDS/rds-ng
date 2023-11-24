<script setup lang="ts">
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { projectActions } from "@/ui/actions/ProjectActions";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectsList from "@/ui/projectslist/ProjectsList.vue";

const comp = FrontendComponent.inject();
const { listProjects } = projectActions(comp);

// When launching the frontend, request all data first
onMounted(() => {
    // Request the projects list after the first render
    nextTick(listProjects);
});
</script>

<template>
    <div class="grid grid-cols-[30rem_1fr] grid-rows-1 gap-0 w-screen h-screen">
        <ProjectsList class="w-full border-e-2 r-border-color" />
        <ProjectDetails class="w-full" />
    </div>
</template>

<style scoped lang="scss">
</style>
