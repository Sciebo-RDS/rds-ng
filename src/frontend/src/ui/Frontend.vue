<script setup lang="ts">
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";

const comp = FrontendComponent.inject();

// When launching the frontend, request all data first
onMounted(() => {
    // Request the projects list after the first render
    nextTick(() => {
        const action = new ListProjectsAction(comp);

        action.prepare();
        action.execute();
    });
});
</script>

<template>
    <router-view />
</template>

<style scoped lang="scss">

</style>
