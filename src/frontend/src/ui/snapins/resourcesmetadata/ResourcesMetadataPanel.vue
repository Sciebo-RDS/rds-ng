<script setup lang="ts">
import { ref, toRefs } from "vue";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import ResourcesTreeTable from "@common/ui/components/resource/ResourcesTreeTable.vue";

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
const selectedNodes = ref({} as Record<string, boolean>);
const resourcesError = ref("");

function refreshResources(): void {
    resourcesError.value = "";

    const action = new ListResourcesAction(comp, true);
    action.prepare(project!.value.resources_path).done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
        } else {
            resourcesNodes.value = [];
            resourcesError.value = msg;
        }
    });
    action.execute();
}
</script>

<template>
    <ResourcesTreeTable
        v-if="!resourcesError"
        :data="resourcesNodes"
        v-model:selected-nodes="selectedNodes"
        class="p-treetable-sm text-sm border border-b-0"
        refreshable
        @refresh="refreshResources"
    />
    <div v-else class="r-text-error">
        The list of objects could not be retrieved from the remote storage: <em>{{ resourcesError }}</em>
    </div>
</template>

<style scoped lang="scss">

</style>
