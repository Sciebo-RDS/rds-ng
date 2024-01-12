<script setup lang="ts">
import { toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);
</script>

<template>
    <div>I AM TEH METADATAAAAA!</div>
</template>

<style scoped lang="scss">

</style>
