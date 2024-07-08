<script setup lang="ts">
import { storeToRefs } from "pinia";
import { reactive, toRefs, watch, type PropType } from "vue";

import { findConnectorByInstanceID } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { Project } from "@common/data/entities/project/Project";
import { MetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/MetadataFeature";
import { ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { type Profile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { PropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import { dataCite } from "@common/ui/components/propertyeditor/profiles/datacite";
import { osf } from "@common/ui/components/propertyeditor/profiles/osf";
import { zenodo } from "@common/ui/components/propertyeditor/profiles/zenodo";

import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    },
    globalObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});
const { project } = toRefs(props);
const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);

// TODO: Testing data only
const mergeSets: PropertySet[] = [];
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
    if (metadataProfile.hasOwnProperty("profile_id")) {
        mergeSets.push(new PropertySet(connector.metadata_profile));
    }
});

const projectObjects = reactive(new ProjectObjectStore());
const projectProfiles = reactive(new PropertyProfileStore());
const debounce = makeDebounce(500);

watch(
    () => project!.value.features.metadata.metadata,
    (metadata) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new MetadataFeature(metadata as ProjectMetadata)]);
            action.execute();
        });
    },
    { deep: true }
);

projectProfiles.mountProfile(dataCite as Profile);
projectProfiles.mountProfile(zenodo as Profile);
projectProfiles.mountProfile(osf as Profile);
</script>

<template>
    <div>
        <PropertyEditor
            v-model="project!.features.metadata.metadata"
            :projectObjects="projectObjects as ProjectObjectStore"
            :globalObjectStore="globalObjectStore as ProjectObjectStore"
            :projectProfiles="projectProfiles as PropertyProfileStore"
        />
    </div>
</template>
