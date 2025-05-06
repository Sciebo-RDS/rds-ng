<script setup lang="ts">
import { type PropType, toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
});
const { project } = toRefs(props);
</script>

<template>
    <div v-if="!!project.description">{{ project.description }}</div>
    <div v-else class="r-text-light italic">The project doesn't have a description.</div>
</template>

<style scoped lang="scss"></style>
