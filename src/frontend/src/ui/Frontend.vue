<script setup lang="ts">
import { Command } from "@common/core/messaging/Command";
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { ListConnectorsAction } from "@/ui/actions/ListConnectorsAction";
import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";

const comp = FrontendComponent.inject();

// When launching the frontend (after the initial render), request all data first
onMounted(() => {
    nextTick(() => {
        // TODO: Merge into single action
        // TODO: Error handling
        const listConAction = new ListConnectorsAction(comp);

        listConAction.prepare().done((cmd: Command, success: boolean, msg: string) => {
            if (success) {
                const listProjAction = new ListProjectsAction(comp);

                listProjAction.prepare();
                listProjAction.execute();
            }
        });

        listConAction.execute();
    });
});
</script>

<template>
    <router-view />
</template>

<style scoped lang="scss">

</style>
