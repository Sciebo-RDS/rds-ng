<script setup lang="ts">
import { Command } from "@common/core/messaging/Command";
import { CommandFailType } from "@common/core/messaging/CommandReply";
import { onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";
import { MessageDialog } from "@/ui/dialogs/MessageDialog";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectList from "@/ui/projectlist/ProjectList.vue";

const comp = FrontendComponent.inject();

function showError(err: string) {
    const msgDlg = new MessageDialog(comp);
    msgDlg.show("Error fetching data", `An error occurred while fetching your data:\n${err}`, "error");
}

// When launching the frontend, request all data first
onMounted(() => {
    // We use a timeout (w/o delay) to do the request after the first render
    setTimeout(() => {
        const statusDlg = new MessageDialog(comp);
        statusDlg.show("Fetching data", "Please wait while your data is being downloaded...", "file_download", false);

        const action = new ListProjectsAction(comp);
        action.prepare().done((cmd: Command, success: boolean, msg: string) => {
            statusDlg.hide();

            if (!success) {
                showError(msg);
            }
        }).failed((failType: CommandFailType, msg: string) => {
            statusDlg.hide();
            showError(msg);
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
