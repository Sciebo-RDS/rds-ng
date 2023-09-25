<script setup lang="ts">
import { useDialog } from "primevue/usedialog";
import { defineAsyncComponent, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ProjectsController } from "@/controllers/ProjectsController";

import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
import ProjectList from "@/ui/projectlist/ProjectList.vue";

const comp = FrontendComponent.inject();
const controller = new ProjectsController(comp);

// When launching the frontend, request all data first
onMounted(() => {
    controller.listProjects();
});

const dialog = comp.vue.config.globalProperties.$dialog;
const FooterDemo = defineAsyncComponent(() => import('@/ui/projectdetails/Header.vue'));

const showProducts = () => {
    const dialogRef = dialog.open(FooterDemo, {});
}
</script>

<template>
    <div class="grid grid-cols-[30rem_1fr] grid-rows-1 gap-0 w-screen h-screen">
        <ProjectList class="w-full border-e-2 r-border-color" @click="showProducts"></ProjectList>
        <ProjectDetails class="w-full"></ProjectDetails>
    </div>
</template>

<style scoped lang="scss">
</style>
