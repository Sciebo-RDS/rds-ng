<script setup lang="ts">
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { ListAllDataAction } from "@/ui/actions/ListAllDataAction";

const comp = FrontendComponent.inject();

// When launching the frontend (after the initial render), request all data first
onMounted(() => {
    nextTick(() => {
        const action = new ListAllDataAction();

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
