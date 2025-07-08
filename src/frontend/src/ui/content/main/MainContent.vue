<script setup lang="ts">
import ProjectDetails from "@/ui/content/main/projectdetails/ProjectDetails.vue";
import ProjectsList from "@/ui/content/main/projectslist/ProjectsList.vue";
</script>

<template>
    <div class="grid grid-cols-[27rem_1fr] grid-rows-1 gap-0 w-screen h-screen bg-surface-0">
        <ProjectsList class="w-full h-full" />
        <ProjectDetails class="w-full h-full" />
    </div>
</template>

<style scoped lang="scss"></style>
