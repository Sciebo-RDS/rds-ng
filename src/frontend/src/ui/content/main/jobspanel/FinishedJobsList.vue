<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, type PropType, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByInstanceID, findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { ProjectLogbookType } from "@common/data/entities/project/logbook/ProjectLogbookType";
import { ProjectJobHistoryRecord } from "@common/data/entities/project/logbook/ProjectJobHistoryRecord";
import { Project } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";
import { getConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { getUnseenProjectJobHistoryRecords } from "@/data/entities/project/ProjectUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";

import { MarkProjectLogbookSeenAction } from "@/ui/actions/project/MarkProjectLogbookSeenAction";

import ProjectJobsPanelItem from "@/ui/content/main/jobspanel/ProjectJobsPanelItem.vue";

interface ListEntry {
    project: Project;
    jobRecord: ProjectJobHistoryRecord;
    connectorInstance: ConnectorInstance | undefined;
    connectorCategory: ConnectorCategory | undefined;
}

const comp = FrontendComponent.inject();
const props = defineProps({
    projects: {
        type: Object as PropType<Project[]>,
        required: true,
    },
});
const { projects } = toRefs(props);
const emits = defineEmits<{
    (e: "changed", entries: ListEntry[]): void;
}>();
const userStore = useUserStore();
const conStore = useConnectorsStore();
const { userSettings } = storeToRefs(userStore);
const { connectors } = storeToRefs(conStore);

const unseenJobRecords = computed(() => {
    const unseenRecords: ListEntry[] = [];
    unref(projects)!.forEach((project) => {
        getUnseenProjectJobHistoryRecords(project).forEach((record) => {
            const connector = findConnectorByInstanceID(unref(connectors), unref(userSettings).connector_instances, record.connector_instance);
            unseenRecords.push({
                project: project,
                jobRecord: record,
                connectorInstance: findConnectorInstanceByID(unref(userSettings).connector_instances, record.connector_instance),
                connectorCategory: connector ? getConnectorCategory(connector) : undefined,
            } as ListEntry);
        });
    });
    unseenRecords.sort((a, b) => b.jobRecord.timestamp - a.jobRecord.timestamp);
    emits("changed", unseenRecords);
    return unseenRecords;
});

function onDismiss(project: Project, record: number): void {
    const action = new MarkProjectLogbookSeenAction(comp, true);
    action.prepare(ProjectLogbookType.JobHistory, false, project, record);
    action.execute();
}

function onDismissAll(): void {
    const action = new MarkProjectLogbookSeenAction(comp, true);
    action.prepare(ProjectLogbookType.JobHistory, true);
    action.execute();
}
</script>

<template>
    <div v-if="unseenJobRecords.length > 0">
        <div class="grid grid-cols-[1fr_auto] r-text-caption border-b">
            <span>Finished jobs</span>
            <div class="grid grid-cols-[min-content_auto] items-center dismiss-all pr-1 r-primary-fg" title="Dismiss all" @click="onDismissAll">
                <span class="material-icons-outlined mi-close !text-lg !leading-none mr-1" />
                <span class="!text-sm">Dismiss all</span>
            </div>
        </div>
        <div class="w-full pt-2">
            <div v-for="(job, index) in unseenJobRecords" :key="index">
                <ProjectJobsPanelItem
                    :index="index"
                    :message="job.jobRecord.message"
                    :result-message="job.jobRecord.success ? 'has succeeded' : 'has failed'"
                    :timestamp="job.jobRecord.timestamp"
                    :severity="job.jobRecord.success ? 'success' : 'error'"
                    :project="job.project"
                    :connector-instance="job.connectorInstance"
                    :connector-category="job.connectorCategory"
                    closable
                    :record="job.jobRecord.record"
                    @dismiss="(record) => onDismiss(job.project, record)"
                />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.dismiss-all {
    @apply cursor-pointer opacity-70;
}

.dismiss-all:hover {
    @apply opacity-100;
}
</style>
