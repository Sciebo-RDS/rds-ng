<script setup lang="ts">
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { FetchAllDataAction } from "@/ui/actions/FetchAllDataAction";

const comp = FrontendComponent.inject();

// When launching the frontend (after the initial render), request all data first
onMounted(() => {
    nextTick(() => {
        const action = new FetchAllDataAction();

        action.prepare(comp);
        action.execute();
    });
});
</script>

<template>
    <router-view />
</template>

<style scoped lang="scss">

</style>
