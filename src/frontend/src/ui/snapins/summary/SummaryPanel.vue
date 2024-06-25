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
    <div>And all in all we can say that this is cool!</div>
</template>

<style scoped lang="scss"></style>
