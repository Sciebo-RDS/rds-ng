<script setup lang="ts">
import BlockUI from "primevue/blockui";
import { reactive, ref, toRefs } from "vue";

import logging from "@common/core/logging/Logging";
import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { resources } from "@common/ui/components/propertyeditor/profiles/resources";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import ResourcesTreeTable from "@common/ui/components/resource/ResourcesTreeTable.vue";

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
const resourcesRefreshing = ref(false);
const resourcesError = ref("");

const resourcesProfile = new PropertySet(resources);
const controller = reactive(new MetadataController(resourcesProfile, [], []));

function refreshResources(): void {
    resourcesRefreshing.value = true;
    resourcesError.value = "";

    const action = new ListResourcesAction(comp, true);
    action.prepare(project!.value.resources_path).done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
        } else {
            resourcesNodes.value = [];
            resourcesError.value = msg;
        }

        resourcesRefreshing.value = false;
    });
    action.execute();
}

const handleMetadataUpdate = (data: PersistedSet[]) => {
};
</script>

<template>
    <BlockUI :blocked="resourcesRefreshing">
        <div v-if="!resourcesError" class="grid grid-cols-2 gap-2 w-full h-full">
            <ResourcesTreeTable
                :data="resourcesNodes"
                v-model:selected-nodes="selectedNodes"
                class="p-treetable-sm text-sm border border-b-0"
                refreshable
                @refresh="refreshResources"
            />

            <div class="border">
                <div class="r-shade-dark-gray r-text-caption-big p-4 border-b"><span>Object Metadata</span></div>
                <PropertyEditor
                    @update="handleMetadataUpdate"
                    :controller="controller as MetadataController"
                    :logging="logging"
                    twoCol
                />

            </div>
        </div>
        <div v-else class="r-text-error">
            The list of objects could not be retrieved from the remote storage: <em>{{ resourcesError }}</em>
        </div>
    </BlockUI>
</template>

<style scoped lang="scss">

</style>
