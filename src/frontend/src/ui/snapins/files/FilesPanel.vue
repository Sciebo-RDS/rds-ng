<script setup lang="ts">
import Column from "primevue/column";
import TreeTable from "primevue/treetable";
import { onMounted, ref, toRefs } from "vue";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";

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

const resourcesNodes = ref<Object[]>([]);
const selectedNodes = ref();
onMounted(() => {
    const action = new ListResourcesAction(comp, true);
    action.prepare().done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
        }
    });
    action.execute();
});
</script>

<template>
    <TreeTable :value="resourcesNodes" selection-mode="multiple" v-model:selectionKeys="selectedNodes" class="p-treetable-sm border border-b-0" auto-layout>
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
    </TreeTable>
</template>

<style scoped lang="scss">

</style>
