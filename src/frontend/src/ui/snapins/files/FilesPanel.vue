<script setup lang="ts">
import { ResourcesList } from "@common/data/entities/resource/ResourcesList";
import Button from "primevue/button";
import Column from "primevue/column";
import TreeTable from "primevue/treetable";
import { onMounted, ref, toRefs } from "vue";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { flattenResourcesList, resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);

const resources = ref<ResourcesList | undefined>(undefined);
const resourcesNodes = ref<Object[]>([]);
const selectedNodes = ref({});
const expandedNodes = ref({});

function refreshResources(): void {
    const action = new ListResourcesAction(comp, true);
    action.prepare().done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resources.value = reply.resources;
            resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
        }
    });
    action.execute();
}

function expandAll(): void {
    if (resources.value) {
        let allResources = {};
        flattenResourcesList(resources.value).forEach((resource) => allResources[resource] = true);
        expandedNodes.value = allResources;
    }
}

function collapseAll(): void {
    expandedNodes.value = {};
}

onMounted(() => refreshResources());
</script>

<template>
    <TreeTable
        :value="resourcesNodes"
        selection-mode="multiple"
        v-model:selectionKeys="selectedNodes"
        v-model:expanded-keys="expandedNodes"
        class="p-treetable-sm border border-b-0"
        auto-layout
        :pt="{
        footer: 'r-shade-gray'
    }">
        <Column field="label" header="Name" class="p-0 pl-2" expander :pt="{ rowToggler: 'mb-1', headerCell: 'r-shade-gray' }">
            <template #body="entry">
                <span :class="entry.node.icon" class="opacity-75 relative top-1.5 mr-1" /><span>{{ entry.node.data.label }}</span>
            </template>
        </Column>

        <Column field="resource" header="Size" :pt="{ headerCell: 'r-shade-gray' }">
            <template #body="entry">
                100kb
            </template>
        </Column>

        <template #footer>
            <div class="flex justify-end gap-2">
                <Button icon="material-icons-outlined mi-keyboard-arrow-down" label="Expand all" size="small" text @click="expandAll" />
                <Button icon="material-icons-outlined mi-keyboard-arrow-right" label="Collapse all" size="small" text @click="collapseAll" />
                <Button icon="material-icons-outlined mi-refresh" label="Refresh" size="small" text severity="warning" @click="refreshResources" />
            </div>
        </template>
    </TreeTable>
</template>

<style scoped lang="scss">

</style>
