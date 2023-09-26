<script setup lang="ts">
import { onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectList from "@/ui/projectlist/ProjectList.vue";

const comp = FrontendComponent.inject();

// When launching the frontend, request all data first
onMounted(() => {
    const action = new ListProjectsAction(comp);
    action.execute();
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
