<script setup lang="ts">
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { MetadataProfileContainerRole } from "@common/data/entities/metadata/MetadataProfileContainer";
import { filterContainers } from "@common/data/entities/metadata/MetadataProfileContainerUtils";
import { storeToRefs } from "pinia";
import { reactive, toRefs, watch, type PropType } from "vue";

import { findConnectorByInstanceID } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { Project } from "@common/data/entities/project/Project";
import { ProjectMetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/ProjectMetadataFeature";
import { type PropertyProfile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";

import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import ProjectExportersBar from "@/ui/components/project/ProjectExportersBar.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

const comp = FrontendComponent.inject();
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
const projectProfiles = reactive(new PropertyProfileStore());

for (const profile of filterContainers(metadataStore.profiles, ProjectMetadataFeature.FeatureID, MetadataProfileContainerRole.Global)) {
    projectProfiles.mountProfile(profile.profile);
}

// TODO fix auto merging connector profiles
connectors.value.forEach((connector) => {
    if (
        !userSettings.value.connector_instances.find((instance) => {
            if (project!.value.options.use_all_connector_instances) {
                return instance.connector_id == connector.connector_id;
            } else {
                return !!project!.value.options.active_connector_instances.find((instanceID) => {
                    const resolvedConnector = findConnectorByInstanceID(connectors.value, userSettings.value.connector_instances, instanceID);
                    return resolvedConnector && resolvedConnector.connector_id == connector.connector_id;
                });
            }
        })
    ) {
        return;
    }

    const metadataProfile = connector.metadata_profile;
    if (metadataProfile.hasOwnProperty("metadata")) {
        try {
            projectProfiles.mountProfile(connector.metadata_profile as PropertyProfile);
        } catch (e) {
            console.error(e);
        }
    }
});

const debounce = makeDebounce();

watch(
    () => project!.value.features.project_metadata.metadata,
    (metadata) => {
        console.log("update");
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new ProjectMetadataFeature(metadata as ProjectMetadata, project!.value.features.project_metadata.shared_objects)]);
            action.execute();
        });
    },
    { deep: true }
);
</script>

<template>
    <ProjectExportersBar :project="project" :scope="ProjectMetadataFeature.FeatureID" class="p-2 grid justify-end" />
    <PropertyEditor
        v-model="project!.features.project_metadata.metadata"
        v-model:shared-objects="project!.features.project_metadata.shared_objects"
        :projectProfiles="projectProfiles as PropertyProfileStore"
    />
</template>
