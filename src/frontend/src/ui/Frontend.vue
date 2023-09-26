<script setup lang="ts">
import { onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";
import { StatusDialog } from "@/ui/dialogs/StatusDialog";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectList from "@/ui/projectlist/ProjectList.vue";

const comp = FrontendComponent.inject();

// When launching the frontend, request all data first
onMounted(() => {
    // We use a timeout (w/o delay) to do the request after the first render
    setTimeout(() => {
        const statusDlg = new StatusDialog(comp);
        statusDlg.show("Fetching data", "Please wait while your data is being downloaded...", "file_download");

        const action = new ListProjectsAction(comp);
        action.prepare().done(() => {
            setTimeout(() => {
                statusDlg.hide();
            }, 1000);
        });
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
