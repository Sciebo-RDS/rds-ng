<script setup lang="ts">
import { nextTick, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { GetAllDataAction } from "@/ui/actions/multi/GetAllDataAction";
import MainContent from "@/ui/content/main/MainContent.vue";

const comp = FrontendComponent.inject();

// When launching the frontend view (after the initial render), get all data first
onMounted(() => {
    nextTick(() => {
        const action = new GetAllDataAction();

        action.prepare(comp);
        action.execute();
    });
});
</script>

<template>
    <MainContent />
</template>

<style scoped lang="scss">

</style>
