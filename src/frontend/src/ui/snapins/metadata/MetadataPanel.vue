<script setup lang="ts">
import { storeToRefs } from "pinia";
import { reactive, ref, toRefs, watch, type PropType } from "vue";

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
import { deepClone } from "@common/utils/ObjectUtils";

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
    }
});
const { project } = toRefs(props);
const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);
const projectProfiles = reactive(new PropertyProfileStore());

// TODO: Testing data only

// TODO fix auto merging connector profiles
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

const debounce = makeDebounce(500);

const projectObjects = ref(new ProjectObjectStore());
projectObjects.value.setObjects(deepClone(project!.value.features.metadata.metadata));

const sharedObjects = ref(new ProjectObjectStore());
sharedObjects.value.setObjects(deepClone(project!.value.features.metadata.shared_objects));

watch(
    () => projectObjects.value._objects,
    (metadata) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new MetadataFeature(metadata as ProjectMetadata, sharedObjects.value._objects as ProjectMetadata)]);
            action.execute();
        });
    },
    { deep: true }
);

watch(
    () => sharedObjects.value._objects,
    (shared_objects) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new MetadataFeature(projectObjects.value._objects as ProjectMetadata, shared_objects)]);
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
            v-model="projectObjects as ProjectObjectStore"
            v-model:shared-objects="sharedObjects as ProjectObjectStore"
            :projectProfiles="projectProfiles as PropertyProfileStore"
        />
    </div>
</template>
