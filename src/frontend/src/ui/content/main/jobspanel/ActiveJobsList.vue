<script setup lang="ts">
import { type PropType, toRefs } from "vue";

import { ProjectJob } from "@common/data/entities/project/ProjectJob";

const props = defineProps({
    jobs: {
        type: Object as PropType<ProjectJob[]>,
        required: true,
    },
});
const { jobs } = toRefs(props);
</script>

<template>
    <div v-if="jobs.length > 0"></div>
    <div v-else class="r-text-light italic grid justify-center">No active jobs running</div>
</template>

<style scoped lang="scss"></style>
