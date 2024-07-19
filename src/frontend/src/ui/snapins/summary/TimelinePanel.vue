<script setup lang="ts">
import { storeToRefs } from "pinia";
import Card from "primevue/card";
import ScrollPanel from "primevue/scrollpanel";
import Timeline from "primevue/timeline";
import { computed, type PropType, toRefs, unref } from "vue";

import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";
import { ProjectJobHistoryRecordExtDataIDs } from "@common/data/entities/project/logbook/ProjectJobHistoryRecord";
import { getJobHistoryRecordExtendedData } from "@common/data/entities/project/logbook/ProjectLogbookUtils";
import { formatLocaleTimestamp } from "@common/utils/Strings";

import { findConnectorCategoryByInstanceID } from "@/data/entities/connector/ConnectorUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";

import ExternalLink from "@common/ui/components/misc/ExternalLink.vue";

const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
});
const { project } = toRefs(props);

const timeline = computed(() => {
    const values = [
        {
            date: formatLocaleTimestamp(unref(project)!.creation_time),
            title: "Project created",
            category: "Creation",
            text: "The project has been created",
            color: "r-bg-info",
            icon: "material-icons mi-flag",
            links: {},
        },
    ];

    unref(project)!.logbook.job_history.forEach((record) => {
        const connectorInstance = findConnectorInstanceByID(unref(userSettings).connector_instances, record.connector_instance);
        const connectorCategory = findConnectorCategoryByInstanceID(unref(connectors), unref(userSettings).connector_instances, record.connector_instance);

        const title =
            (record.success
                ? `Successfully ${connectorCategory?.verbStatusDone.toLowerCase() || "exported"}`
                : `Failed to ${connectorCategory?.verbAction.toLowerCase() || "export"}`) + ` to ${connectorInstance?.name || "Unknown connection"}`;

        const links: Record<string, string> = {};
        const projectLink = getJobHistoryRecordExtendedData(record, ProjectJobHistoryRecordExtDataIDs.ExternalLink);
        if (projectLink) {
            links["Project link"] = projectLink;
        }

        values.unshift({
            date: formatLocaleTimestamp(record.timestamp),
            title: title,
            category: connectorCategory?.verbNoun || "Export",
            text: record.message,
            color: record.success ? "r-bg-success" : "r-bg-error",
            icon: "material-icons " + (record.success ? "mi-rocket-launch" : "mi-error"),
            links: links,
        });
    });

    return values;
});
</script>

<template>
    <ScrollPanel class="w-full h-full">
        <Timeline :value="timeline" :pt="{ opposite: 'max-w-fit', separator: 'pt-1', content: 'pt-0.5' }">
            <template #marker="entry">
                <span class="flex w-8 h-8 items-center justify-center text-white rounded-full z-1" :class="entry.item.color">
                    <i :class="entry.item.icon"></i>
                </span>
            </template>

            <template #opposite="entry">
                <div class="grid grid-flow-row">
                    <span class="p-text-secondary text-sm font-semibold">{{ entry.item.date }}</span>
                    <span class="p-text-secondary text-sm font-normal">{{ entry.item.category }}</span>
                </div>
            </template>

            <template #content="entry">
                <Card class="mt-3 mb-3.5" :pt="{ body: 'gap-2' }">
                    <template #title>
                        <span class="text-lg">{{ entry.item.title }}</span>
                    </template>

                    <template #content>
                        <span>{{ entry.item.text }}</span>
                    </template>

                    <template v-if="Object.entries(entry.item.links).length > 0" #footer>
                        <div class="grid grid-flow-row pt-2">
                            <span v-for="(link, title) in entry.item.links" class="text-slate-600 text-sm">
                                <span class="font-semibold pr-1">{{ title }} &#x2022;</span>
                                <ExternalLink :link="link" />
                            </span>
                        </div>
                    </template>
                </Card>
            </template>
        </Timeline>
    </ScrollPanel>
</template>

<style scoped lang="scss"></style>
