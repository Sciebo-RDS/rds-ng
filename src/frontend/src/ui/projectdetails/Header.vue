<script setup lang="ts">
import { toRefs } from "vue";

import { Project } from "@common/data/entities/Project";

const props = defineProps({
    project: {
        type: Project
    }
});
const { project } = toRefs(props);
</script>

<template>
    <div v-if="project" class="grid grid-rows-2 grid-cols-[1fr_min-content] grid-flow-col gap-x-2 place-content-center justify-start r-primary-bg r-primary-text pl-3">
        <div class="text-lg font-bold self-center pt-3">
            {{ project.title }}
        </div>
        <div class="italic self-center pb-3">I do not have a path yet</div>
    </div>
    <div v-else class="r-primary-bg r-primary-text grid content-center justify-center">
        <div class="r-text-caption-big r-small-caps">No project selected</div>
    </div>
</template>

<style scoped lang="scss">
</style>
