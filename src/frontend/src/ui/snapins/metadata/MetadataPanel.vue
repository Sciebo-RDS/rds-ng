<script setup lang="ts">
import { storeToRefs } from "pinia";
import { type PropType, reactive, toRefs, watch } from "vue";

import logging from "@common/core/logging/Logging";
import { findConnectorByInstanceID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";
import { MetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/MetadataFeature";
import { testProfile } from "@common/ui/components/propertyeditor/DummyData";
import { dataCite } from "@common/ui/components/propertyeditor/profiles/datacite";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { type PropertyProfile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
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
        mergeSets.push(new PropertySet(connector.metadata_profile as PropertyProfile));
    }
});

const baseSet = new PropertySet(dataCite);
const profiles: PropertySet[] = [new PropertySet(testProfile)];
const controller = reactive(new MetadataController(baseSet, mergeSets, profiles));

watch(
    () => project!.value.features.metadata.metadata,
    (metadata) => {
        const action = new UpdateProjectFeaturesAction(comp);
        action.prepare(project!.value, [new MetadataFeature(metadata as ProjectMetadata)]);
        action.execute();
    },
);
</script>

<template>
    <div>
        <PropertyEditor
            v-model="project!.features.metadata.metadata as PersistedSet[]"
            :controller="controller as MetadataController"
            :logging="logging"
            twoCol
        />
    </div>
</template>

<style scoped lang="scss"></style>
