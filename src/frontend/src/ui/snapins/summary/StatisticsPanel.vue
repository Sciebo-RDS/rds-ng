<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import { findConnectorCategoryByInstanceID } from "@/data/entities/connector/ConnectorUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { ListResourcesReply } from "@common/api/resource/ResourceCommands";

import { Project } from "@common/data/entities/project/Project";
import { ProjectStatistics } from "@common/data/entities/project/ProjectStatistics";
import { ResourcesStatistics } from "@common/data/entities/resource/ResourcesStatistics";
import { formatLocaleTimestamp, humanReadableFileSize } from "@common/utils/Strings";
import { storeToRefs } from "pinia";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import ScrollPanel from "primevue/scrollpanel";
import { computed, onMounted, type PropType, ref, toRefs, unref } from "vue";

const comp = FrontendComponent.inject();
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

const resourcesStatistics = ref<ResourcesStatistics | undefined>(undefined);

function refreshResources(): void {
    const action = new ListResourcesAction(comp, true);
    action.prepare(project!.value.resources_path).done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resourcesStatistics.value = new ResourcesStatistics(reply.resources);
        } else {
            resourcesStatistics.value = undefined;
        }
    });
    action.execute();
}

onMounted(() => refreshResources());

const values = computed(() => {
    const projStatistics = new ProjectStatistics(unref(project));
    const totalJobStatistics = projStatistics.getTotalJobStatistics();
    const values = [
        // General
        {
            group: "General",
            name: "Project ID",
            value: unref(project)!.project_id,
        },
        {
            group: "General",
            name: "Created on",
            value: formatLocaleTimestamp(unref(project)!.creation_time),
        },
        // Publish and export
        {
            group: "Publish & Export",
            name: "Total publications and exports",
            value: `${totalJobStatistics.totalCount.succeeded} total (${totalJobStatistics.totalCount.failed} failed)`,
        },
        {
            group: "Publish & Export",
            name: "Last published or exported on",
            value: totalJobStatistics.lastJob > 0 ? formatLocaleTimestamp(totalJobStatistics.lastJob) : "Never",
        },
    ];

    // Connector instances
    for (const instance of unref(userSettings).connector_instances.sort((a, b) => a.name.localeCompare(b.name))) {
        const succeeded = projStatistics.getJobStatistics(instance.instance_id).totalCount.succeeded;
        const failed = projStatistics.getJobStatistics(instance.instance_id).totalCount.failed;
        const category = findConnectorCategoryByInstanceID(unref(connectors), unref(userSettings).connector_instances, instance.instance_id);

        values.push({
            group: "Publish & Export",
            name: instance.name,
            value: `${succeeded} ${category ? (succeeded > 1 ? category.verbNounPlural : category.verbNoun) : ""} (${failed} failed)`,
        });
    }

    let totalNumberOfObjects = "";
    let totalSizeOfObjects = "";
    if (!!unref(resourcesStatistics)) {
        const statistics = unref(resourcesStatistics)!.getResourcesStatistics();
        totalNumberOfObjects = `${statistics.totalFileCount} file(s) in ${statistics.totalFolderCount} folder(s)`;
        totalSizeOfObjects = humanReadableFileSize(statistics.totalSize);
    }

    values.push(
        // Objects
        {
            group: "Objects",
            name: "Data path",
            value: unref(project)!.resources_path,
        },
        {
            group: "Objects",
            name: "Total number of objects",
            value: totalNumberOfObjects,
        },
        {
            group: "Objects",
            name: "Total size of objects",
            value: totalSizeOfObjects,
        },
    );

    return values;
});
</script>

<template>
    <ScrollPanel class="h-full">
        <DataTable
            :value="values"
            rowGroupMode="subheader"
            groupRowsBy="group"
            class="border rounded"
            :pt="{ rowGroupHeader: 'r-shade-dark-gray', thead: 'hidden' }"
        >
            <Column field="group" />
            <Column field="name" header="Name" class="w-80" />
            <Column field="value" header="Value" body-class="italic" />

            <template #groupheader="slotProps">
                <div class="r-text-caption">
                    <span>{{ slotProps.data.group }}</span>
                </div>
            </template>
        </DataTable>
    </ScrollPanel>
</template>

<style scoped lang="scss"></style>
