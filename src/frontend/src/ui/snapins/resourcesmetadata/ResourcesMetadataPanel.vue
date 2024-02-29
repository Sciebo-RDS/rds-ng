<script setup lang="ts">
import BlockUI from "primevue/blockui";
import Button from "primevue/button";
import Image from "primevue/image";
import { nextTick, reactive, ref, toRefs, watch } from "vue";

import logging from "@common/core/logging/Logging";
import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { type ResourcesMetadata, ResourcesMetadataFeature } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { resources } from "@common/ui/components/propertyeditor/profiles/resources";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import { extractPersistedSetFromArray, intersectPersistedSets } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";
import { deepClone } from "@common/utils/ObjectUtils";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import ResourcesTreeTable from "@common/ui/components/resource/ResourcesTreeTable.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";

import previewImage from "@assets/img/preview.png";

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
const resourcesData = ref<PersistedSet[]>([]);
const controller = reactive(new MetadataController(resourcesProfile, [], []));

const showPreview = ref(true);

let blockResourcesUpdate = false;

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

watch(resourcesData, (metadata) => {
    if (blockResourcesUpdate) {
        return;
    }

    const resourcesSet = extractPersistedSetFromArray(metadata, resources.profile_id);
    const updatedData = deepClone<ResourcesMetadata>(project!.value.features.resources_metadata.resources_metadata);

    const selectedPaths = Object.keys(selectedNodes.value);
    selectedPaths.forEach((path) => {
        updatedData[path] = resourcesSet;
    });

    const action = new UpdateProjectFeaturesAction(comp);
    action.prepare(project!.value, [new ResourcesMetadataFeature(updatedData)]);
    action.execute();

    // TODO: A hack to update the local data; nedds to be changed later
    project!.value.features.resources_metadata.resources_metadata = updatedData;
});

watch(selectedNodes, (nodes: Record<string, boolean>) => {
    blockResourcesUpdate = true;

    const persistedSets: PersistedSet[] = [];
    const selectedPaths = Object.keys(nodes);
    const metadata = project!.value.features.resources_metadata.resources_metadata;
    selectedPaths.forEach((path) => {
        persistedSets.push(path in metadata ? (metadata[path] as PersistedSet) : new PersistedSet(resources.profile_id, {}));
    });

    resourcesData.value = [intersectPersistedSets(persistedSets, resources.profile_id)];

    // Unblock only after the resources watcher had a chance to fire
    nextTick(() => blockResourcesUpdate = false);
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
                <div class="grid grid-cols-[1fr_min-content] items-center r-shade-dark-gray r-text-caption-big p-2.5 border-b">
                    <span>Object Metadata</span>
                    <span>
                        <Button
                            icon="material-icons-outlined mi-visibility"
                            title="Toggle preview"
                            size="small"
                            :severity="showPreview ? '' : 'secondary'"
                            text
                            rounded
                            @click="showPreview = !showPreview"
                        />
                    </span>
                </div>

                <div v-if="Object.keys(selectedNodes).length > 0" class="grid grid-flow-rows grid-cols-1 justify-items-center w-full">
                    <div v-if="showPreview" class="mt-5">
                        <Image :src="previewImage" alt="Preview" title="This is just a placeholder..." class="border rounded-2xl" width="200" preview />
                    </div>
                    <PropertyEditor
                        v-model="resourcesData"
                        :controller="controller as MetadataController"
                        :logging="logging"
                        oneCol
                        class="w-full"
                    />
                </div>
                <div v-else class="r-centered-grid italic pt-8">Select one or more file objects on the left to edit their metadata.</div>
            </div>
        </div>
        <div v-else class="r-text-error">
            The list of objects could not be retrieved from the remote storage: <em>{{ resourcesError }}</em>
        </div>
    </BlockUI>
</template>

<style scoped lang="scss"></style>
