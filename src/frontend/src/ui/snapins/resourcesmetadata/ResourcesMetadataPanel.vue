<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import Panel from "primevue/panel";
import ScrollPanel from "primevue/scrollpanel";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import ToggleSwitch from "primevue/toggleswitch";
import { computed, nextTick, onMounted, type PropType, ref, toRefs, unref, watch } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { getOptionalMetadataProfiles } from "@common/data/entities/project/ProjectUtils.ts";
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { useResourcesStore } from "@/data/stores/ResourcesStore.ts";
import { useUserStore } from "@/data/stores/UserStore.ts";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools.ts";

import MetadataProfilesSelector from "@/ui/components/metadata/MetadataProfilesSelector.vue";
import ProjectExportersBar from "@/ui/components/project/ProjectExportersBar.vue";
import ResourcesPreview from "@/ui/snapins/resourcesmetadata/ResourcesPreview.vue";

import { MetadataProfileContainerRole } from "@common/data/entities/metadata/MetadataProfileContainer";
import { filterContainers, isContainerSelected } from "@common/data/entities/metadata/MetadataProfileContainerUtils";
import { ResourcesMetadata, ResourcesMetadataFeature, type ResourcesMetadataKey } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { Project } from "@common/data/entities/project/Project";
import { Resource } from "@common/data/entities/resource/Resource";
import { adjustResourcesTreeNodesLeafStates, resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { type ProfileID } from "@common/ui/components/propertyeditor/PropertyProfile.ts";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";
import { deepClone } from "@common/utils/ObjectUtils";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import ResourcesTreeTable from "@common/ui/components/resource/ResourcesTreeTable.vue";

const comp = FrontendComponent.inject();
const resourcesStore = useResourcesStore();
const metadataStore = useMetadataStore();
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);

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

const enabledProfiles = ref<ProfileID[]>(unref(project).features.resources_metadata.enabled_metadata_profiles);
const metadataProfiles = computed(() => {
    const profileStore = new PropertyProfileStore();

    for (const profile of filterContainers(metadataStore.profiles, ResourcesMetadataFeature.FeatureID, [
        MetadataProfileContainerRole.Default,
        MetadataProfileContainerRole.Optional
    ])) {
        if (isContainerSelected(profile, unref(enabledProfiles))) {
            profileStore.mountProfile(profile.profile);
        }
    }

    return profileStore;
});
const optionalProfiles = computed(() =>
    getOptionalMetadataProfiles(unref(project), unref(userSettings), [], metadataStore.profiles, ResourcesMetadataFeature.FeatureID)
);

const resourcesData = ref();

const debounce = makeDebounce();
let blockResourcesUpdate = false;

onMounted(() => {
    // Initiate the retrieval of the project directory; if this has been done before, it will be fetched from the cache automatically
    retrieveDataPath(unref(project).resources_path);
});

function saveProject(): void {
    debounce(() => {
        const action = new UpdateProjectFeaturesAction(comp);
        action.prepare(unref(project), [new ResourcesMetadataFeature(unref(project).features.resources_metadata.metadata, unref(enabledProfiles))]);
        action.execute();
    });
}

function retrieveDataPath(path: string): void {
    resourcesError.value = "";

    const root = unref(project).resources_path;
    retrieveResourcesList(root, path, false)
        .then(() => {
            const resources = unref(resourcesListCache).root(root).resources;
            if (!!resources) {
                const nodes = resourcesListToTreeNodes(resources);
                resourcesNodes.value = adjustResourcesTreeNodesLeafStates(nodes, resources, (path: string) =>
                    unref(resourcesListCache).root(root).contains(path)
                );
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

watch(
    () => resourcesData,
    (metadata) => {
        if (blockResourcesUpdate) {
            return;
        }

        debounce(() => {
            const resourcesSet = unref(metadata);
            const updatedData = deepClone<ResourcesMetadata>(unref(project).features.resources_metadata.metadata);

            const selectedPaths = Object.keys(selectedNodes.value);
            selectedPaths.forEach((path: ResourcesMetadataKey) => {
                updatedData[path as ResourcesMetadataKey] = resourcesSet;
            });

            // TODO: A hack to update the local data; needs to be changed later
            // @ts-ignore
            project.value.features.resources_metadata.metadata = updatedData;

            saveProject();
        });
    },
    { deep: true }
);

watch(selectedNodes, (nodes: Record<string, boolean>) => {
    blockResourcesUpdate = true;

    const selectedPaths = Object.keys(nodes);
    const metadata = unref(project).features.resources_metadata.metadata;

    resourcesData.value = metadata[selectedPaths[0]!] || [];

    // Unblock only after the resources watcher had a chance to fire
    nextTick(() => (blockResourcesUpdate = false));
});
watch(enabledProfiles, saveProject);
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
                        <div v-if="optionalProfiles.length > 0" class="pt-2 pl-2 pr-4 w-full">
                            <MetadataProfilesSelector :profiles="optionalProfiles" v-model:selected-profiles="enabledProfiles" class="h-min" />
                        </div>
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
                            v-model:shared-property-objects="project.features.shared_objects"
                            :projectProfiles="metadataProfiles"
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
