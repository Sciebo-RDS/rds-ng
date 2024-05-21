<script setup lang="ts">
import NewProject from "@/ui/content/main/projectslist/NewProject.vue";
import ProjectsListbox from "@/ui/content/main/projectslist/ProjectsListbox.vue";
</script>

<template>
    <div class="grid grid-rows-[1fr_6rem] grid-cols-1 r-shade-gray">
        <ProjectsListbox />
        <NewProject />
    </div>
</template>

<style scoped lang="scss"></style>
