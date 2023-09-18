<script setup lang="ts">
import ProjectList from "@/ui/projectlist/ProjectList.vue";
import ProjectDetails from "@/ui/projectdetails/ProjectDetails.vue";
</script>

<template>
    <div class="grid grid-cols-[30rem_1fr] grid-rows-1 gap-0 w-screen h-screen">
        <ProjectList class="w-full border-e-2 r-border-color"></ProjectList>
        <ProjectDetails class="w-full"></ProjectDetails>
    </div>
</template>

<style scoped lang="scss">
</style>
