<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { ListResourcesReply } from "@common/api/resource/ResourceCommands";

import { Project } from "@common/data/entities/project/Project";
import { ResourcesStatistics } from "@common/data/entities/resource/ResourcesStatistics";
import { formatLocaleTimestamp, humanReadableFileSize } from "@common/utils/Strings";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import ScrollPanel from "primevue/scrollpanel";
import { computed, onMounted, type PropType, ref, toRefs, unref } from "vue";

const comp = FrontendComponent.inject();
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

const values = ref([
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
        value: 100,
    },
    {
        group: "Publish & Export",
        name: "OSF (Test Account)",
        value: 90,
    },
    {
        group: "Publish & Export",
        name: "Stubby!",
        value: 10,
    },
    // Objects
    {
        group: "Objects",
        name: "Data path",
        value: unref(project)!.resources_path,
    },
    {
        group: "Objects",
        name: "Total number of objects",
        value: computed(() => {
            if (!!unref(resourcesStatistics)) {
                const statistics = unref(resourcesStatistics)!.getResourcesStatistics();
                return `${statistics.totalFileCount} file(s) in ${statistics.totalFolderCount} folder(s)`;
            } else {
                return "";
            }
        }),
    },
    {
        group: "Objects",
        name: "Total size of objects",
        value: computed(() => {
            return !!unref(resourcesStatistics) ? humanReadableFileSize(unref(resourcesStatistics)!.getResourcesStatistics().totalSize) : "";
        }),
    },
]);
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
