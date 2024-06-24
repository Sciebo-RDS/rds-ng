<script setup lang="ts">
import BlockUI from "primevue/blockui";
import Button from "primevue/button";
import Image from "primevue/image";
import InputSwitch from "primevue/inputswitch";
import Panel from "primevue/panel";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import { computed, nextTick, reactive, ref, toRefs, watch, type PropType } from "vue";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { Project } from "@common/data/entities/project/Project";
import { ResourcesMetadataFeature, type ResourcesMetadata } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { Profile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { resources } from "@common/ui/components/propertyeditor/profiles/resources";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";
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
    },
    globalObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});
const { project } = toRefs(props);

const resourcesNodes = ref<Object[]>([]);
const selectedNodes = ref({} as Record<string, boolean>);
const resourcesRefreshing = ref(false);
const resourcesError = ref("");

/* const resourcesProfile = new PropertySet(resources);
const controller = reactive(new MetadataController(resourcesProfile, [], [])); */

const resourcesData = ref();

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

const propertyHeader = computed(() => {
    switch (Object.keys(selectedNodes.value).length) {
        case 0:
            return "Object Metadata";
        case 1:
            return Object.keys(selectedNodes.value)[0];
        default:
            return `${Object.keys(selectedNodes.value).length} objects selected`;
    }
});

const projectObjects = reactive(new ProjectObjectStore());
const projectProfiles = reactive(new PropertyProfileStore());
const debounce = makeDebounce(500);

watch(
    resourcesData,
    (metadata) => {
        if (blockResourcesUpdate) {
            return;
        }

        debounce(() => {
            const resourcesSet = metadata;
            const updatedData = deepClone<ResourcesMetadata>(project!.value.features.resources_metadata.resources_metadata);

            const selectedPaths = Object.keys(selectedNodes.value);
            selectedPaths.forEach((path) => {
                updatedData[path] = resourcesSet;
            });
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new ResourcesMetadataFeature(updatedData)]);
            action.execute();

            // TODO: A hack to update the local data; nedds to be changed later
            // @ts-ignore
            project!.value.features.resources_metadata.resources_metadata = updatedData;
        });
    },
    { deep: true }
);

watch(selectedNodes, (nodes: Record<string, boolean>) => {
    blockResourcesUpdate = true;

    /* const persistedSets: PersistedSet[] = []; */
    const selectedPaths = Object.keys(nodes);
    const metadata = project!.value.features.resources_metadata.resources_metadata;
    /* selectedPaths.forEach((path) => {
        persistedSets.push(path in metadata ? (metadata[path] as PersistedSet) : new PersistedSet(resources.profile_id, {}));
    }); */

    resourcesData.value = metadata[selectedPaths[0]] || [];

    // Unblock only after the resources watcher had a chance to fire
    nextTick(() => (blockResourcesUpdate = false));
});

projectProfiles.mountProfile(resources as Profile);
const showObjects = ref(false);
const showIndex = ref(true);
</script>

<template>
    <BlockUI :blocked="resourcesRefreshing" class="h-full">
        <div v-if="!resourcesError" class="h-full">
            <Splitter state-key="resources-splitter-state" class="h-full rounded-none border-0">
                <SplitterPanel :size="50" :min-size="35">
                    <ResourcesTreeTable
                        :data="resourcesNodes"
                        v-model:selected-nodes="selectedNodes"
                        class="p-treetable-sm text-sm border border-b-0 h-full"
                        refreshable
                        @refresh="refreshResources"
                    />
                </SplitterPanel>

                <SplitterPanel :size="50" :min-size="25">
                    <div class="overflow-auto h-full">
                        <div class="grid grid-cols-[1fr_min-content] items-center r-shade-gray r-text-caption-big p-2.5 border-b pb-[0.7rem]">
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
                                <Panel class="mx-5 mt-5">
                                    <template #header>
                                        <span class="flex w-full mx-2 gap-2">
                                            <span class="grow font-bold">
                                                <i class="pi pi-exclamation-circle mr-2" /> Changes will apply to
                                                {{ Object.keys(selectedNodes).length }} objects.
                                            </span>
                                            <label for="switch1">Show Objects</label> <InputSwitch v-model="showObjects" />
                                        </span>
                                    </template>
                                    <div v-if="showObjects">
                                        <div class="m-2 mt-0 flex gap-2 flex-row-reverse">
                                            <InputSwitch v-model="showIndex" input-id="switch1" /> <label for="switch1">Show Index</label>
                                        </div>
                                        <div class="m-2 p-2 rounded bg-gray-100">
                                            <p
                                                v-for="[i, path] of Object.keys(selectedNodes).sort().entries()"
                                                class="m-0 font-mono text-ellipsis overflow-hidden text-nowrap"
                                                :title="path"
                                            >
                                                {{ showIndex ? i + 1 : null }} {{ path }}
                                            </p>
                                        </div>
                                    </div>
                                </Panel>
                            </div>
                            <div v-else-if="showPreview" class="mt-5">
                                <Image :src="previewImage" alt="Preview" title="This is just a placeholder..." class="border rounded-2xl" width="200" preview />
                            </div>
                            <PropertyEditor
                                v-model="resourcesData"
                                :projectObjects="projectObjects as ProjectObjectStore"
                                :globalObjectStore="globalObjectStore as ProjectObjectStore"
                                :projectProfiles="projectProfiles as PropertyProfileStore"
                                class="w-full"
                            />
                        </div>
                        <div v-else class="r-centered-grid italic pt-8">Select one or more file objects on the left to edit their metadata.</div>
                    </div>
                </SplitterPanel>
            </Splitter>
        </div>
        <div v-else class="r-text-error p-2">
            <div class="font-bold">The list of objects could not be retrieved from the remote storage:</div>
            <div class="italic">{{ resourcesError }}</div>
        </div>
    </BlockUI>
</template>

<style scoped lang="scss"></style>
