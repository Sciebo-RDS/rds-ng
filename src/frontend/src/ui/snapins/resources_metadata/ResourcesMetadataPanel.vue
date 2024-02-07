<script setup lang="ts">
import { ref, toRefs } from "vue";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { type Resource } from "@common/data/entities/resource/Resource";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import ResourcesTreeTable from "@common/ui/components/ResourcesTreeTable.vue";

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
const selectedNodes = ref({} as Record<Resource, boolean>);

function refreshResources(): void {
    const action = new ListResourcesAction(comp, true);
    action.prepare(project!.value.resource).done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
        }
    });
    action.execute();
}
</script>

<template>
    <ResourcesTreeTable
        :data="resourcesNodes"
        v-model:selected-nodes="selectedNodes"
        class="p-treetable-sm border border-b-0"
        refreshable
        @refresh="refreshResources"
    />
</template>

<style scoped lang="scss">

</style>
