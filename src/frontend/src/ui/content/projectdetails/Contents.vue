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
    <div v-if="project" class="m-3">
        {{ project.description }}
    </div>
    <div v-else>
    </div>
</template>

<style scoped lang="scss">

</style>
