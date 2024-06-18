<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, shallowReactive } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { GetAllDataAction } from "@/ui/actions/multi/GetAllDataAction";

import MainContent from "@/ui/content/main/MainContent.vue";

const comp = FrontendComponent.inject();
const integrationScheme = shallowReactive(comp.integrationScheme);

onMounted(() => {
    // When launching the frontend view (after the initial render), get all data first
    nextTick(() => {
        const action = new GetAllDataAction();

        action.prepare(comp);
        action.completed(() => {
            // The app has been fully integrated; notify the authentication scheme about this
            integrationScheme.beginSession();
        });
        action.execute();
    });
});
onUnmounted(() => {
    // The app is about to abandon the integration; notify the authentication scheme about this
    integrationScheme.endSession();
});
</script>

<template>
    <MainContent />
</template>

<style scoped lang="scss"></style>
