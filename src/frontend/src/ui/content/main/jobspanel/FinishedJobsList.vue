<script setup lang="ts">
import Button from "primevue/button";
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
    return unseenRecords.sort((a, b) => b.jobRecord.timestamp - a.jobRecord.timestamp);
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
    <div class="r-text-caption border-b">Finished jobs</div>
    <div v-if="unseenJobRecords.length > 0" class="w-full pt-2">
        <div v-for="(job, index) in unseenJobRecords" :key="index">
            <ProjectJobsPanelItem
                :index="index"
                :message="job.jobRecord.message"
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

        <Button
            label="Dismiss all"
            size="small"
            icon="material-icons-outlined mi-close !text-lg"
            text
            class="float-right mt-2 px-2 py-0.5 !text-sm"
            @click="onDismissAll"
        />
    </div>
    <div v-else class="r-text-light italic grid justify-center">No finished jobs</div>
</template>

<style scoped lang="scss"></style>
