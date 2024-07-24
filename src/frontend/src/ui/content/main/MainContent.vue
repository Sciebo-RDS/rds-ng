<script setup lang="ts">
import ProjectDetails from "@/ui/content/main/projectdetails/ProjectDetails.vue";
import ProjectsList from "@/ui/content/main/projectslist/ProjectsList.vue";
</script>

<template>
    <div class="grid grid-cols-[30rem_1fr] grid-rows-1 gap-0 w-screen h-screen">
        <ProjectsList class="w-full border-e-2 r-border-color h-full" />
        <ProjectDetails class="w-full h-full" />
    </div>
</template>

<style scoped lang="scss"></style>
