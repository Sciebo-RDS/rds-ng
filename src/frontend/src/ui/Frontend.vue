<script setup lang="ts">
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { GetAllDataAction } from "@/ui/actions/multi/GetAllDataAction";

const comp = FrontendComponent.inject();

// When launching the frontend (after the initial render), get all data first
onMounted(() => {
    nextTick(() => {
        const action = new GetAllDataAction();

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
