<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, type PropType, toRefs, unref } from "vue";

import { ProjectJob } from "@common/data/entities/project/ProjectJob";
import { formatElapsedTime } from "@common/utils/Strings";

import { getAllProjectJobDetails, type ProjectJobDetails } from "@/data/entities/project/ProjectJobUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

import ProjectJobsPanelItem from "@/ui/content/main/jobspanel/ProjectJobsPanelItem.vue";

const props = defineProps({
    jobs: {
        type: Object as PropType<ProjectJob[]>,
        required: true,
    },
});
const { jobs } = toRefs(props);
const emits = defineEmits<{
    (e: "changed", entries: ProjectJobDetails[]): void;
}>();
const projStore = useProjectsStore();
const userStore = useUserStore();
const conStore = useConnectorsStore();
const { projects } = storeToRefs(projStore);
const { userSettings } = storeToRefs(userStore);
const { connectors } = storeToRefs(conStore);

const runningJobs = computed(() => {
    const details = getAllProjectJobDetails(unref(projects), unref(jobs), unref(connectors), unref(userSettings).connector_instances);
    emits("changed", details);
    return details;
});
</script>

<template>
    <div v-if="jobs.length > 0">
        <div class="r-text-caption border-b">Active jobs</div>
        <div class="w-full pt-2">
            <div v-for="(job, index) in runningJobs" :key="index">
                <div class="grid grid-cols-[1fr_min-content]" :class="{ 'pt-2': index != 0 }">
                    <ProjectJobsPanelItem
                        :index="index"
                        :message="job.job.message"
                        result-message="is currently running"
                        :timestamp="job.job.timestamp"
                        severity="info"
                        :project="job.project"
                        :connector-instance="job.connectorInstance"
                        :connector-category="job.connectorCategory"
                        :progress="job.job.progress"
                        :elapsed="formatElapsedTime(new Date().getTime() / 1000 - job.job.timestamp)"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
