<script setup lang="ts">
import ScrollPanel from "primevue/scrollpanel";
import { type PropType, ref, toRefs } from "vue";

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
const activeJobsEmpty = ref(true);
const finishedJobsEmpty = ref(true);
</script>

<template>
    <ScrollPanel class="w-full h-full min-w-[30rem] max-h-[60vh]">
        <div class="w-full h-full overflow-auto grid grid-flow-row content-start">
            <div v-if="activeJobsEmpty && finishedJobsEmpty" class="r-centered-grid">
                <div class="r-text-light italic">There currently are no active or finished jobs</div>
            </div>

            <ActiveJobsList :jobs="jobs" @changed="(entries) => (activeJobsEmpty = entries.length == 0)" />
            <div v-if="!activeJobsEmpty && !finishedJobsEmpty" class="h-5">&nbsp;</div>
            <FinishedJobsList :projects="projects" @changed="(entries) => (finishedJobsEmpty = entries.length == 0)" />
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
