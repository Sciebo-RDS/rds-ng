<script setup lang="ts">
import { storeToRefs } from "pinia";
import Card from "primevue/card";
import { computed, type PropType, ref, toRefs, unref, watch } from "vue";

import { MetadataProfileContainerRole } from "@common/data/entities/metadata/MetadataProfileContainer";
import { filterContainers, filterContainersByRoles, isContainerSelected } from "@common/data/entities/metadata/MetadataProfileContainerUtils";
import { ProjectMetadataFeature } from "@common/data/entities/project/features/ProjectMetadataFeature";
import { Project } from "@common/data/entities/project/Project";
import { getOptionalMetadataProfiles, isConnectorActivated } from "@common/data/entities/project/ProjectUtils.ts";
import { type ProfileID } from "@common/ui/components/propertyeditor/PropertyProfile.ts";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import LinkedText from "@common/ui/components/misc/LinkedText.vue";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { useUserStore } from "@/data/stores/UserStore";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
import { useUserTools } from "@/ui/tools/user/UserTools.ts";

import MetadataProfilesSelector from "@/ui/components/metadata/MetadataProfilesSelector.vue";
import ProjectExportersBar from "@/ui/components/project/ProjectExportersBar.vue";

const comp = FrontendComponent.inject();
const { editUserSettings } = useUserTools(comp);
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    }
});
const { project } = toRefs(props);
const metadataStore = useMetadataStore();
const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);

const enabledProfiles = ref<ProfileID[]>(unref(project).features.project_metadata.enabled_metadata_profiles);
const metadataProfiles = computed(() => {
    const profileStore = new PropertyProfileStore();

    for (const profile of filterContainers(metadataStore.profiles, ProjectMetadataFeature.FeatureID, [
        MetadataProfileContainerRole.Default,
        MetadataProfileContainerRole.Optional
    ])) {
        if (isContainerSelected(profile, unref(enabledProfiles))) {
            profileStore.mountProfile(profile.profile);
        }
    }

    connectors.value.forEach((connector) => {
        if (isConnectorActivated(unref(project), unref(userSettings), connector, unref(connectors))) {
            for (const profile of filterContainersByRoles(connector.metadata_profiles, [
                MetadataProfileContainerRole.Default,
                MetadataProfileContainerRole.Optional
            ])) {
                if (isContainerSelected(profile, unref(enabledProfiles))) {
                    profileStore.mountProfile(profile.profile);
                }
            }
        }
    });

    return profileStore;
});
const optionalProfiles = computed(() =>
    getOptionalMetadataProfiles(unref(project), unref(userSettings), unref(connectors), metadataStore.profiles, ProjectMetadataFeature.FeatureID)
);

const debounce = makeDebounce();

function saveProject(): void {
    debounce(() => {
        const action = new UpdateProjectFeaturesAction(comp);
        action.prepare(unref(project), [new ProjectMetadataFeature(unref(project).features.project_metadata.metadata, unref(enabledProfiles))]);
        action.execute();
    });
}

watch(() => unref(project).features.project_metadata.metadata, saveProject, { deep: true });
watch(enabledProfiles, saveProject);
</script>

<template>
    <div v-if="userSettings.connector_instances.length == 0" class="p-2 px-6">
        <Card class="bg-amber-100 text-amber-700 !p-0 mt-4 ml-auto mr-auto w-max" :pt="{ title: '!text-base', caption: 'h-5', body: 'p-3 px-5' }">
            <template #title>
                <div class="flex items-center gap-1">
                    <span class="material-icons-outlined mi-link-off !text-xl" />
                    <span class="">No connections added</span>
                </div>
            </template>
            <template #content>
                <span class="text-sm">
                    You haven't configured any connections to external services yet. In order to add metadata to your project, open your
                    <LinkedText text="settings" @click="() => editUserSettings(userSettings)" icon-class="material-icons-outlined mi-settings" />
                    and add at least one connection.
                </span>
            </template>
        </Card>
    </div>
    <div v-else>
        <div class="grid grid-cols-[1fr_max-content] gap-10 px-1 pt-1 h-min">
            <MetadataProfilesSelector
                v-if="optionalProfiles.length > 0"
                :profiles="optionalProfiles"
                v-model:selected-profiles="enabledProfiles"
                class="h-min"
            />
            <div v-else>&nbsp;</div>

            <ProjectExportersBar :project="project" :scope="ProjectMetadataFeature.FeatureID" class="p-2 justify-self-end" />
        </div>
        <PropertyEditor
            v-model="project.features.project_metadata.metadata"
            v-model:shared-property-objects="project.features.shared_objects"
            :projectProfiles="metadataProfiles"
        />
    </div>
</template>

<style scoped lang="scss"></style>
