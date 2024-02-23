<script setup lang="ts">
import { toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

import ProjectControls from "@/ui/content/main/projectdetails/ProjectControls.vue";

const props = defineProps({
    project: {
        type: Project,
        required: true,
    },
});
const { project } = toRefs(props);
</script>

<template>
    <div class="grid grid-rows-2 grid-cols-[1fr_max-content] grid-flow-col gap-x-2 place-content-center justify-start r-primary-bg r-primary-text p-3">
        <div class="text-xl font-bold self-center truncate text-ellipsis" :title="project!.title">
            {{ project!.title }}
        </div>
        <div class="italic self-center truncate text-ellipsis" :title="project!.resources_path"><b>Data path: </b>{{ project!.resources_path }}</div>
        <div class="row-span-2 self-center">
            <ProjectControls :project="project!" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
