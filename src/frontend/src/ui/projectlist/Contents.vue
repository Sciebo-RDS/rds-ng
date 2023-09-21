<script setup lang="ts">
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ListProjectsCommand, ListProjectsCommandReply } from "@common/api/ProjectCommands";
import { networkStore } from "@common/data/stores/NetworkStore";

const comp = FrontendComponent.inject();

function listProjects() {
    console.log("Fetching projects...");

    const store = networkStore();
    const builder = comp.frontendService.messageBuilder;

    builder.buildCommand(ListProjectsCommand).done((cmd: ListProjectsCommandReply, success: boolean, msg: string) => {
        console.log("Projects reply:");
        console.log(cmd.projects);
    }).emit(store.serverChannel);
}
</script>

<template>
    <div class="r-shade r-shade-text p-1.5">
        <Button title="Fetch projects" @click="listProjects">Fetch projects</Button>
    </div>
</template>

<style scoped lang="scss">

</style>
