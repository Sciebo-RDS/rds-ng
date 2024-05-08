<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import InlineMessage from "primevue/inlinemessage";
import { computed, type PropType, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByInstanceID, findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { ProjectJobHistoryRecord } from "@common/data/entities/project/logbook/ProjectJobHistoryRecord";
import { Project } from "@common/data/entities/project/Project";
import { formatLocaleTimestamp } from "@common/utils/Strings";

import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";
import { getConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { getUnseenProjectJobHistoryRecords } from "@/data/entities/project/ProjectUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";

interface ListEntry {
    project: Project;
    jobRecord: ProjectJobHistoryRecord;
    connectorInstance: ConnectorInstance | undefined;
    connectorCategory: ConnectorCategory | undefined;
}

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
    return unseenRecords;
});
</script>

<template>
    <div v-if="unseenJobRecords.length > 0" class="w-full">
        <div v-for="(job, index) in unseenJobRecords" :key="index">
            <div class="grid grid-cols-[1fr_min-content] px-1 group" :class="{ 'pt-2': index != 0 }">
                <InlineMessage :severity="job.jobRecord.success ? 'success' : 'error'" class="flex w-full justify-start" :pt="{ text: 'w-full !text-sm' }">
                    <div>
                        <div class="grid grid-cols-[1fr_auto] items-center text-gray-700 mb-1 w-full">
                            <div class="font-normal">{{ job.connectorCategory?.verbNoun || "Export" }}</div>
                            <div class="mr-2 font-light text-xs">{{ formatLocaleTimestamp(job.jobRecord.timestamp) }}</div>
                        </div>
                        <div class="font-bold">
                            {{ job.project.title }} &rarr;
                            {{ job.connectorInstance?.name || "Unknown connection" }}
                        </div>
                        <div>{{ job.jobRecord.message }}</div>
                    </div>
                </InlineMessage>
                <div class="ml-1.5 mt-0.5 invisible" :class="{ 'group-hover:visible': true }">
                    <Button
                        icon="material-icons-outlined mi-close"
                        severity="secondary"
                        rounded
                        outlined
                        size="small"
                        title="Dismiss"
                        :pt="{ root: 'w-8 h-8', icon: '!text-lg' }"
                    />
                </div>
            </div>
        </div>
    </div>
    <div v-else class="r-text-light italic grid justify-center">No finished jobs</div>
</template>

<style scoped lang="scss"></style>
