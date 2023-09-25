<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import { ProjectsController } from "@/controllers/ProjectsController";
import Button from "primevue/button";

const comp = FrontendComponent.inject();

function listProjects() {
    console.log("Fetching projects...");

    const controller = new ProjectsController(comp.frontendService);
    controller.listProjects();
}
</script>

<template>
    <div class="r-shade r-shade-text p-1.5">
        <Button title="Fetch projects" @click="listProjects">Fetch projects</Button>
    </div>
</template>

<style scoped lang="scss">

</style>
