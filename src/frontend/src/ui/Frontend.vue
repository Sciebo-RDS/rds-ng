<script setup lang="ts">
import { onMounted } from "vue";

import { ErrorDialogNotifier } from "@/ui/actions/notifiers/ErrorDialogNotifier";
import { ExecutionDialogNotifier } from "@/ui/actions/notifiers/ExecutionDialogNotifier";
import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";

import { FrontendComponent } from "@/component/FrontendComponent";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectList from "@/ui/projectlist/ProjectList.vue";

const comp = FrontendComponent.inject();

// When launching the frontend, request all data first
onMounted(() => {
    // We use a timeout (w/o delay) to do the request after the first render
    setTimeout(() => {
        const action = new ListProjectsAction(comp.frontendService, [
            new ExecutionDialogNotifier("Fetching projects", "Please wait while your projects are being downloaded...", "file_download"),
            new ErrorDialogNotifier("Error fetching projects", "An error occurred while downloading your projects"),
        ]);
        action.prepare();
        action.execute();
    });
});
</script>

<template>
    <div class="grid grid-cols-[30rem_1fr] grid-rows-1 gap-0 w-screen h-screen">
        <ProjectList class="w-full border-e-2 r-border-color"></ProjectList>
        <ProjectDetails class="w-full"></ProjectDetails>
    </div>
</template>

<style scoped lang="scss">
</style>
