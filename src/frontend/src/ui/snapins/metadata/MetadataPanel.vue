<script setup lang="ts">
import { storeToRefs } from "pinia";
import { reactive, toRefs, watch, type PropType } from "vue";

import { findConnectorByInstanceID } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { Project } from "@common/data/entities/project/Project";
import { MetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/MetadataFeature";
import { type Profile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { dataCite } from "@common/ui/components/propertyeditor/profiles/datacite";

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
const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);
const projectProfiles = reactive(new PropertyProfileStore());

projectProfiles.mountProfile(dataCite as Profile);
// TODO: Testing data only

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
            projectProfiles.mountProfile(connector.metadata_profile as Profile);
        } catch (e) {
            console.error(e);
        }
    }
});

const debounce = makeDebounce(500);

watch(
    () => project!.value.features.metadata.metadata,
    (metadata) => {
        console.log("update");
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new MetadataFeature(metadata as ProjectMetadata, project!.value.features.metadata.shared_objects)]);
            action.execute();
        });
    },
    { deep: true }
);
</script>

<template>
    <ProjectExportersBar :project="project" :scope="MetadataFeature.FeatureID" class="p-2 grid justify-end" />
    <PropertyEditor
        v-model="project!.features.metadata.metadata"
        v-model:shared-objects="project!.features.metadata.shared_objects"
        :projectProfiles="projectProfiles as PropertyProfileStore"
    />
</template>
