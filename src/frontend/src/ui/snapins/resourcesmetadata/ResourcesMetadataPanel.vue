<script setup lang="ts">
import { useResourcesStore } from "@/data/stores/ResourcesStore.ts";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools.ts";
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import Panel from "primevue/panel";
import ScrollPanel from "primevue/scrollpanel";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import ToggleSwitch from "primevue/toggleswitch";
import { computed, nextTick, onMounted, type PropType, reactive, ref, toRefs, unref, watch } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

import ProjectExportersBar from "@/ui/components/project/ProjectExportersBar.vue";
import ResourcesPreview from "@/ui/snapins/resourcesmetadata/ResourcesPreview.vue";

import { MetadataProfileContainerRole } from "@common/data/entities/metadata/MetadataProfileContainer";
import { filterContainers } from "@common/data/entities/metadata/MetadataProfileContainerUtils";
import { ResourcesMetadata, ResourcesMetadataFeature, type ResourcesMetadataKey } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { Project } from "@common/data/entities/project/Project";
import { Resource } from "@common/data/entities/resource/Resource";
import { adjustResourcesTreeNodesLeafStates, resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";
import ResourcesTreeTable from "@common/ui/components/resource/ResourcesTreeTable.vue";
import { deepClone } from "@common/utils/ObjectUtils";

const comp = FrontendComponent.inject();
const resourcesStore = useResourcesStore();
const metadataStore = useMetadataStore();

const { retrieveResourcesList } = useResourceTools(comp);
const { resourcesListCache } = storeToRefs(resourcesStore);

const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    }
});
const { project } = toRefs(props);

const resourcesNodes = ref<Object[]>([]);
const selectedNodes = ref({} as Record<string, boolean>);
const selectedData = ref([] as Array<Resource>);
const resourcesError = ref("");

const showPreview = ref(true);
const showObjects = ref(true);

const propertyHeader = computed(() => {
    switch (Object.keys(selectedNodes.value).length) {
        case 0:
            return "Object metadata";
        case 1:
            return Object.keys(selectedNodes.value)[0];
        default:
            return `${Object.keys(selectedNodes.value).length} objects selected`;
    }
});

const projectProfiles = reactive(new PropertyProfileStore());
const debounce = makeDebounce();
const resourcesData = ref();

let blockResourcesUpdate = false;

onMounted(() => {
    for (const profile of filterContainers(metadataStore.profiles, ResourcesMetadataFeature.FeatureID, MetadataProfileContainerRole.Global)) {
        projectProfiles.mountProfile(profile.profile);
    }

    // Initiate the retrieval of the root directory; if this has been done before, it will be fetched from the cache automatically
    retrieveDataPath("");
});

watch(
    () => resourcesData,
    (metadata) => {
        if (blockResourcesUpdate) {
            return;
        }

        debounce(() => {
            const resourcesSet = unref(metadata);
            const updatedData = deepClone<ResourcesMetadata>(project!.value.features.resources_metadata.metadata);

            const selectedPaths = Object.keys(selectedNodes.value);
            selectedPaths.forEach((path: ResourcesMetadataKey) => {
                updatedData[path as ResourcesMetadataKey] = resourcesSet;
            });
            const action = new UpdateProjectFeaturesAction(comp);
            console.log(resourcesSet);
            action.prepare(project!.value, [new ResourcesMetadataFeature(updatedData)]);
            action.execute();

            // TODO: A hack to update the local data; needs to be changed later
            // @ts-ignore
            project!.value.features.resources_metadata.metadata = updatedData;
        });
    },
    { deep: true }
);

watch(selectedNodes, (nodes: Record<string, boolean>) => {
    blockResourcesUpdate = true;

    /* const persistedSets: PersistedSet[] = []; */
    const selectedPaths = Object.keys(nodes);
    const metadata = project!.value.features.resources_metadata.metadata;
    /* selectedPaths.forEach((path) => {
        persistedSets.push(path in metadata ? (metadata[path] as PersistedSet) : new PersistedSet(resources.profile_id, {}));
    }); */

    resourcesData.value = metadata[selectedPaths[0]] || [];

    // Unblock only after the resources watcher had a chance to fire
    nextTick(() => (blockResourcesUpdate = false));
});

function retrieveDataPath(path: string): void {
    resourcesError.value = "";

    retrieveResourcesList(path, false)
        .then(() => {
            const resources = unref(resourcesListCache).resources;
            if (!!resources) {
                const nodes = resourcesListToTreeNodes(resources);
                resourcesNodes.value = adjustResourcesTreeNodesLeafStates(nodes, resources, (path: string) => unref(resourcesListCache).contains(path));
            } else {
                resourcesNodes.value = [];
            }
        })
        .catch((reason: string) => {
            resourcesError.value = reason;
        });
}

function onDataPathNodeExpand(path: string): void {
    if (!!path) {
        retrieveDataPath(path);
    }
}
</script>

<template>
    <div v-if="!resourcesError" class="h-full">
        <ProjectExportersBar :project="project" :scope="ResourcesMetadataFeature.FeatureID" class="p-2 grid justify-end" />
        <Splitter state-key="resources-splitter-state" class="h-full rounded-none border-0">
            <SplitterPanel :size="50" :min-size="35">
                <ResourcesTreeTable
                    :data="resourcesNodes"
                    v-model:selected-nodes="selectedNodes"
                    v-model:selected-data="selectedData"
                    class="p-treetable-sm text-sm border border-b-0 h-full"
                    dynamic
                    expand-first-only
                    @node-expand="onDataPathNodeExpand"
                />
            </SplitterPanel>

            <SplitterPanel :size="50" :min-size="25">
                <ScrollPanel class="h-full">
                    <div class="grid grid-cols-[1fr_min-content] items-center r-shade-gray r-text-caption-big p-2.5 border-b pb-[0.7rem] h-[3.85rem]">
                        <span class="truncate mx-1" :title="Object.keys(selectedNodes).sort().join('\n')"> {{ propertyHeader }}</span>
                        <span>
                            <Button
                                v-if="Object.keys(selectedNodes).length == 1"
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
                        <div v-if="Object.keys(selectedNodes).length > 1" class="w-full">
                            <Panel
                                class="mx-5 mt-5"
                                :pt="{
                                    content: () => {
                                        return showObjects ? '' : 'h-0';
                                    }
                                }"
                            >
                                <template #header>
                                    <span class="flex w-full gap-2">
                                        <span class="grow font-bold">
                                            <i class="pi pi-exclamation-circle mr-2" /> Changes will be applied to
                                            {{ Object.keys(selectedNodes).length }} objects.
                                        </span>
                                        <label for="switch1">Show objects</label> <ToggleSwitch v-model="showObjects" />
                                    </span>
                                </template>
                                <div v-if="showObjects">
                                    <div class="p-2 rounded bg-gray-100">
                                        <p
                                            v-for="[i, path] of Object.keys(selectedNodes).sort().entries()"
                                            class="m-0 font-mono text-ellipsis overflow-hidden text-nowrap"
                                            :title="path"
                                        >
                                            {{ path }}
                                        </p>
                                    </div>
                                </div>
                                <div v-else class="h-0" />
                            </Panel>
                        </div>
                        <div v-else-if="showPreview" class="mt-5">
                            <ResourcesPreview :resources="selectedData" />
                        </div>
                        <PropertyEditor
                            v-model="resourcesData"
                            v-model:shared-property-objects="project!.features.shared_objects"
                            :projectProfiles="projectProfiles as PropertyProfileStore"
                            class="w-full"
                            :show-profile-tags="false"
                        />
                    </div>
                    <div v-else class="r-centered-grid italic p-8">Select one or more file objects on the left to edit their metadata.</div>
                </ScrollPanel>
            </SplitterPanel>
        </Splitter>
    </div>
    <div v-else class="r-text-error p-2">
        <div class="font-bold">The list of objects could not be retrieved from the remote storage:</div>
        <div class="italic">{{ resourcesError }}</div>
    </div>
</template>

<style scoped lang="scss"></style>
