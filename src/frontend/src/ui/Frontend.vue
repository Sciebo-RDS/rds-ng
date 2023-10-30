<script setup lang="ts">
import { onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectsList from "@/ui/projectslist/ProjectsList.vue";

const comp = FrontendComponent.inject();

// When launching the frontend, request all data first
onMounted(() => {
    // We use a timeout (w/o delay) to do the request after the first render
    setTimeout(() => {
        const action = new ListProjectsAction(comp);

        action.prepare();
        action.execute();
    });
});
</script>

<template>
    <div class="grid grid-cols-[30rem_1fr] grid-rows-1 gap-0 w-screen h-screen">
        <ProjectsList class="w-full border-e-2 r-border-color"/>
        <ProjectDetails class="w-full"/>
    </div>
</template>

<style scoped lang="scss">
</style>
