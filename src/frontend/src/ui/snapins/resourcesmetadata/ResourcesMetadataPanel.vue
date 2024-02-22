<script setup lang="ts">
import BlockUI from "primevue/blockui";
import { ref, toRefs, watch } from "vue";

import logging from "@common/core/logging/Logging";
import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { type ResourcesMetadata, ResourcesMetadataFeature } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { resources } from "@common/ui/components/propertyeditor/profiles/resources";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import { extractPersistedSetFromArray, intersectPersistedSets } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import ResourcesTreeTable from "@common/ui/components/resource/ResourcesTreeTable.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
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
const resourcesRefreshing = ref(false);
const resourcesError = ref("");

const resourcesProfile = new PropertySet(resources);
const controller = ref<MetadataController | undefined>(undefined);
const controllerKey = ref(0); // TODO: Just a workaround for missing reactivity

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

function refreshMetadataController(resourcesData?: PersistedSet): void {
    const resourcesProfile = new PropertySet(resources, resourcesData);
    controller.value = new MetadataController(resourcesProfile, [], []);

    // TODO: This forces the PropertyEditor to be recreated
    controllerKey.value += 1;
}

function handleMetadataUpdate(data: PersistedSet[]): void {
    const resourcesData = extractPersistedSetFromArray(data, resources.profile_id);
    const selectedPaths = Object.keys(selectedNodes.value);
    selectedPaths.forEach((path) => {
        // TODO: Just a quick hack, perform update in a better way later
        project!.value.features.resources_metadata.resources_metadata[path] = resourcesData;
    });

    const action = new UpdateProjectFeaturesAction(comp);
    action.prepare(project!.value, [new ResourcesMetadataFeature(project!.value.features.resources_metadata.resources_metadata as ResourcesMetadata)]);
    action.execute();
}

watch(selectedNodes, (nodes: Record<string, boolean>) => {
    const persistedSets: PersistedSet[] = [];
    const selectedPaths = Object.keys(nodes);
    const metadata = project!.value.features.resources_metadata.resources_metadata;
    selectedPaths.forEach((path) => {
        persistedSets.push(path in metadata ? metadata[path] as PersistedSet : new PersistedSet(resources.profile_id, {}));
    });
    const resourcesData = intersectPersistedSets(persistedSets, resources.profile_id);

    refreshMetadataController(resourcesData);
});
</script>

<template>
    <BlockUI :blocked="resourcesRefreshing">
        <div v-if="!resourcesError" class="grid grid-cols-2 gap-2 w-full h-full">
            <ResourcesTreeTable
                :data="resourcesNodes"
                v-model:selected-nodes="selectedNodes"
                class="p-treetable-sm text-sm border border-b-0 mb-auto"
                refreshable
                @refresh="refreshResources"
            />

            <div class="border">
                <div class="r-shade-dark-gray r-text-caption-big p-4 border-b"><span>Object Metadata</span></div>
                <PropertyEditor
                    v-if="Object.keys(selectedNodes).length > 0"
                    :key="controllerKey"
                    @update="handleMetadataUpdate"
                    :controller="controller as MetadataController"
                    :logging="logging"
                    twoCol
                />
                <div v-else class="r-centered-grid italic pt-8">
                    Select one or more file objects on the left to edit their metadata.
                </div>
            </div>
        </div>
        <div v-else class="r-text-error">
            The list of objects could not be retrieved from the remote storage: <em>{{ resourcesError }}</em>
        </div>
    </BlockUI>
</template>

<style scoped lang="scss">

</style>
