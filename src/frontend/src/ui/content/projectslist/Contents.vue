<script setup lang="ts">
import NewProject from "@/ui/content/projectslist/NewProject.vue";
import ProjectsListbox from "@/ui/content/projectslist/ProjectsListbox.vue";
</script>

<template>
    <div class="grid grid-rows-[1fr_6rem] grid-cols-1 r-shade">
        <ProjectsListbox />
        <NewProject />
    </div>
</template>

<style scoped lang="scss"></style>
