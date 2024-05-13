<script setup lang="ts">
import ScrollPanel from "primevue/scrollpanel";
import { type PropType, toRefs } from "vue";

import { ProjectJob } from "@common/data/entities/project/ProjectJob";
import { Project } from "@common/data/entities/project/Project";

import ActiveJobsList from "@/ui/content/main/jobspanel/ActiveJobsList.vue";
import FinishedJobsList from "@/ui/content/main/jobspanel/FinishedJobsList.vue";

const props = defineProps({
    projects: {
        type: Object as PropType<Project[]>,
        required: true,
    },
    jobs: {
        type: Object as PropType<ProjectJob[]>,
        required: true,
    },
});
const { projects, jobs } = toRefs(props);
</script>

<template>
    <ScrollPanel class="w-full h-full min-w-[30rem] max-h-[60vh]">
        <div class="w-full h-full overflow-auto grid grid-flow-row content-start">
            <ActiveJobsList :jobs="jobs" />
            <div class="h-5">&nbsp;</div>
            <FinishedJobsList :projects="projects" />
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss">
.dismiss-all {
    @apply opacity-75;
}

.dismiss-all:hover {
    @apply opacity-100 cursor-pointer;
}
</style>
