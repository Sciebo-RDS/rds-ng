<script setup lang="ts">
import { storeToRefs } from "pinia";
import InlineMessage from "primevue/inlinemessage";
import { computed, type PropType, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { ProjectJobHistoryRecord } from "@common/data/entities/project/logbook/ProjectJobHistoryRecord";
import { Project } from "@common/data/entities/project/Project";

import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { getUnseenProjectJobHistoryRecords } from "@/data/entities/project/ProjectUtils";
import { useUserStore } from "@/data/stores/UserStore";

interface JobRecordEntry {
    project: Project;
    record: ProjectJobHistoryRecord;
    connectorInstance: ConnectorInstance | undefined;
}

const props = defineProps({
    projects: {
        type: Object as PropType<Project[]>,
        required: true,
    },
});
const { projects } = toRefs(props);
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);

const unseenJobRecords = computed(() => {
    const unseenRecords: JobRecordEntry[] = [];
    unref(projects)!.forEach((project) => {
        getUnseenProjectJobHistoryRecords(project).forEach((record) => {
            unseenRecords.push({
                project: project,
                record: record,
                connectorInstance: findConnectorInstanceByID(unref(userSettings).connector_instances, record.connector_instance),
            } as JobRecordEntry);
        });
    });
    return unseenRecords;
});
</script>

<template>
    <div v-if="unseenJobRecords.length > 0" class="w-full">
        <div v-for="(job, index) in unseenJobRecords" :key="index">
            <div class="px-1" :class="{ 'pt-2': index != 0 }">
                <InlineMessage :severity="job.record.success ? 'success' : 'error'" class="flex w-full justify-start">
                    <div>{{ job.project.title }} &rarr; {{ job.connectorInstance?.name || "Unknown connection" }}</div>
                    <div class="font-normal">{{ job.record.message }}</div>
                </InlineMessage>
            </div>
        </div>
    </div>
    <div v-else class="r-text-light italic grid justify-center">No finished jobs</div>
</template>

<style scoped lang="scss"></style>
