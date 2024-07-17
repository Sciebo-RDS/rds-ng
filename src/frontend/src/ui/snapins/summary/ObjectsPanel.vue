<script setup lang="ts">
import ScrollPanel from "primevue/scrollpanel";
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
    <ScrollPanel class="h-full">Coming soon</ScrollPanel>
</template>

<style scoped lang="scss"></style>
